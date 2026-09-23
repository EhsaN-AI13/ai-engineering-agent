from agent.agent import EhsaNAgent
from agent.tool_executor import ToolExecutor
from tools.definitions import calculator_definition, count_words_definition
from agent.tool_registry import ToolRegistry
from logger import logger
from agent.tool_selector import ToolSelector
from agent.llm import LLM
from agent.memory import ConversationMemory
from openai import RateLimitError
from unittest.mock import Mock
import json

class MockLLM:

    def __init__(self, registry):
        self.registry = registry

    def run(self, user_input):
        import re

        if "ضربدر" in user_input or "*" in user_input:
            operation = "multiply"

        elif "جمع" in user_input or "+" in user_input:
            operation = "add"

        elif "منهای" in user_input or "-" in user_input:
            operation = "subtract"

        elif "تقسیم" in user_input or "/" in user_input:
            operation = "divide"

        else:
            return "پاسخ نامشخص"

        numbers = re.findall(r"\d+(?:\.\d+)?", user_input)

        a = float(numbers[0])
        b = float(numbers[1])

        result = self.registry.get("calculator")(
            a,
            b,
            operation
        )

        if result.is_integer():
            result = int(result)

        return f"نتیجه: {result}"
def create_test_agent():
    agent = EhsaNAgent()
    agent.llm = MockLLM(agent.registry)
    return agent


def test_agent_name():
    agent = EhsaNAgent()
    assert agent.name == "EhsaN"


def test_agent_calculate():
    agent = EhsaNAgent()
    result = agent.calculate(10, 5, "multiply")
    assert result == 50


def test_agent_multiply():
    agent = create_test_agent()
    result = agent.run("10 ضربدر 5 چقدر میشه؟")
    assert result == "نتیجه: 50"


def test_agent_add():
    agent = create_test_agent()
    result = agent.run("10 جمع 5 چقدر میشه؟")
    assert result == "نتیجه: 15"


def test_agent_subtract():
    agent = create_test_agent()
    result = agent.run("10 منهای 5 چقدر میشه؟")
    assert result == "نتیجه: 5"


def test_agent_divide():
    agent = create_test_agent()
    result = agent.run("10 تقسیم بر 5 چقدر میشه؟")
    assert result == "نتیجه: 2"



def test_agent_math_symbols():
    agent = create_test_agent()

    assert agent.run("2*10") == "نتیجه: 20"
    assert agent.run("20+5") == "نتیجه: 25"
    assert agent.run("100-30") == "نتیجه: 70"
    assert agent.run("50/5") == "نتیجه: 10"

def test_calculator_tool_registered():
    agent = create_test_agent()

    assert "calculator" in agent.tools
    assert callable(agent.tools["calculator"])

def test_tool_executor():
    agent = EhsaNAgent()
    executor = ToolExecutor(agent.tools)

    result = executor.execute(
        "calculator",
        10,
        5,
        "multiply"
    )

    assert result == 50


def test_calculator_definition():
    assert calculator_definition["name"] == "calculator"

    assert "description" in calculator_definition

    assert "parameters" in calculator_definition

    assert calculator_definition["parameters"]["properties"]["operation"]["enum"] == [
    "add",
    "subtract",
    "multiply",
    "divide"
] 

def test_tool_registry():
    registry = ToolRegistry()

    assert registry.list_tools() == [
        "calculator",
        "count_words",
        "get_current_time",
        "read_file"
        
    ]

def test_tool_registry_get_count_words():
    registry = ToolRegistry()

    count_words_tool = registry.get("count_words")

    assert callable(count_words_tool)
    assert count_words_tool("hello world") == 2


def test_tool_registry_get_calculator():
    registry = ToolRegistry()

    calculator = registry.get("calculator")

    assert callable(calculator)
    assert calculator(10, 5, "multiply") == 50


def test_tool_executor_unknown_tool():
    agent = EhsaNAgent()
    executor = ToolExecutor(agent.registry)

    result = executor.execute(
        "unknown_tool",
        10,
        5
    )

    assert result == "Tool error: Tool 'unknown_tool' not found."

def test_tool_registry_unknown_tool():
    registry = ToolRegistry()

    try:
        registry.get("unknown_tool")
        assert False
    except ValueError as error:
        assert str(error) == "Tool 'unknown_tool' not found."

from tools.text_tool import count_words

def test_count_words():
    result = count_words("hello world from EhsaN")

    assert result == 4


def test_agent_count_words():
    agent = EhsaNAgent()

    result = agent.count_words("hello world from EhsaN")

    assert result == 4

def test_count_words_definition():
    assert count_words_definition["name"] == "count_words"

    assert "description" in count_words_definition

    assert "parameters" in count_words_definition

    assert count_words_definition["parameters"]["properties"]["text"]["type"] == "string"


def test_tool_registry_get_calculator_definition():
    registry = ToolRegistry()

    definition = registry.get_definition("calculator")

    assert definition["name"] == "calculator"


def test_tool_registry_get_count_words_definition():
    registry = ToolRegistry()

    definition = registry.get_definition("count_words")

    assert definition["name"] == "count_words"
    assert definition["parameters"]["properties"]["text"]["type"] == "string"

def test_tool_registry_list_definitions():
    registry = ToolRegistry()

    assert registry.list_definitions() == [
        "calculator",
        "count_words",
        "get_current_time",
        "read_file"
        
    ]


def test_tool_registry_unknown_definition():
    registry = ToolRegistry()

    try:
        registry.get_definition("unknown_tool")
        assert False
    except ValueError as error:
        assert str(error) == "Definition for tool 'unknown_tool' not found."

def test_tool_registry_get_all_definitions():
    registry = ToolRegistry()

    definitions = registry.get_all_definitions()

    assert len(definitions) == 4
    assert definitions[0]["name"] == "calculator"
    assert definitions[1]["name"] == "count_words"


def test_agent_get_tool_definitions():
    agent = EhsaNAgent()

    definitions = agent.get_tool_definitions()

    assert len(definitions) == 4
    assert definitions[0]["name"] == "calculator"
    assert definitions[1]["name"] == "count_words"

def test_tool_selector():
    registry = ToolRegistry()

    selector = ToolSelector(registry)

    assert selector.registry is registry

def test_tool_selector_count_words():
    registry = ToolRegistry()
    selector = ToolSelector(registry)

    result = selector.select("تعداد کلمات hello world")

    assert result == "count_words"


def test_tool_selector_calculator():
    registry = ToolRegistry()
    selector = ToolSelector(registry)

    result = selector.select("10 ضربدر 5")

    assert result == "calculator"


def test_tool_selector_unknown():
    registry = ToolRegistry()
    selector = ToolSelector(registry)

    result = selector.select("سلام حالت چطوره؟")

    assert result is None

def test_tool_executor_kwargs():
    registry = ToolRegistry()
    executor = ToolExecutor(registry)

    result = executor.execute(
        "calculator",
        a=10,
        b=5,
        operation="multiply"
    )

    assert result == 50

def test_llm_execute_tool():
    registry = ToolRegistry()
    llm = LLM(registry)

    result = llm._execute_tool(
        "calculator",
        {
            "a": 10,
            "b": 5,
            "operation": "multiply"
        }
    )

    assert result == 50


def test_llm_execute_current_time():
    registry = ToolRegistry()
    llm = LLM(registry)

    result = llm._execute_tool(
        "get_current_time",
        {}
    )

    assert isinstance(result, str)

def test_llm_execute_count_words():
    registry = ToolRegistry()
    llm = LLM(registry)

    result = llm._execute_tool(
        "count_words",
        {
            "text": "hello world from EhsaN"
        }
    )

    assert result == 4

def test_llm_tool_call_cycle():
    registry = ToolRegistry()
    llm = LLM(registry)

    class MockResponse:
        def __init__(self, output, response_id="test-response"):
            self.output = output
            self.id = response_id
            self.output_text = "نتیجه نهایی: 50"

    class MockFunctionCall:
        type = "function_call"
        name = "calculator"
        arguments = '{"a": 10, "b": 5, "operation": "multiply"}'
        call_id = "call_123"

    responses = [
        MockResponse([MockFunctionCall()]),
        MockResponse([], "final-response")
    ]

    class MockResponses:
        def __init__(self):
            self.calls = 0

        def create(self, **kwargs):
            response = responses[self.calls]
            self.calls += 1
            return response

    llm.client.responses = MockResponses()

    result = llm.run("10 ضربدر 5 چند می‌شود؟")

    assert result == "نتیجه نهایی: 50"

def test_llm_multiple_tool_calls():
    registry = ToolRegistry()
    llm = LLM(registry)

    class MockResponse:
        def __init__(self, output, response_id, output_text=""):
            self.output = output
            self.id = response_id
            self.output_text = output_text

    class MockFunctionCall:
        def __init__(self, name, arguments, call_id):
            self.type = "function_call"
            self.name = name
            self.arguments = arguments
            self.call_id = call_id

    responses = [
        MockResponse(
            [
                MockFunctionCall(
                    "calculator",
                    '{"a": 10, "b": 5, "operation": "multiply"}',
                    "call_1"
                )
            ],
            "response_1"
        ),
        MockResponse(
            [
                MockFunctionCall(
                    "count_words",
                    '{"text": "hello world from EhsaN"}',
                    "call_2"
                )
            ],
            "response_2"
        ),
        MockResponse(
            [],
            "response_3",
            "هر دو ابزار با موفقیت اجرا شدند."
        )
    ]

    class MockResponses:
        def __init__(self):
            self.calls = 0

        def create(self, **kwargs):
            response = responses[self.calls]
            self.calls += 1
            return response

    llm.client.responses = MockResponses()

    result = llm.run("اول 10 ضربدر 5 را حساب کن، بعد تعداد کلمات را بشمار.")

    assert result == "هر دو ابزار با موفقیت اجرا شدند."
    assert llm.client.responses.calls == 3


def test_llm_includes_web_search_tool():
    registry = ToolRegistry()
    llm = LLM(registry)

    class MockResponse:
        def __init__(self):
            self.output = []
            self.id = "response_1"
            self.output_text = "mock answer"

    class MockResponses:
        def __init__(self):
            self.kwargs = None

        def create(self, **kwargs):
            self.kwargs = kwargs
            return MockResponse()

    mock_responses = MockResponses()
    llm.client.responses = mock_responses

    result = llm.run("آخرین نسخه Python چیست؟")

    assert result == "mock answer"

    tools = mock_responses.kwargs["tools"]

    assert {"type": "web_search"} in tools


def test_llm_get_tools():
    registry = ToolRegistry()
    llm = LLM(registry)

    tools = llm._get_tools()

    assert len(tools) == 5

    assert {"type": "web_search"} in tools



def test_llm_get_tools_does_not_modify_registry():
    registry = ToolRegistry()
    llm = LLM(registry)

    original_definitions = registry.get_all_definitions()

    tools = llm._get_tools()

    assert len(original_definitions) == 4
    assert len(tools) == 5
    assert {"type": "web_search"} in tools

def test_tool_executor_handles_tool_error():
    registry = ToolRegistry()
    executor = ToolExecutor(registry)

    result = executor.execute(
        "calculator",
        10,
        0,
        "divide"
    )

    assert result == "Tool error: Cannot divide by zero."


def test_conversation_memory():
    memory = ConversationMemory()

    memory.add_user_message("سلام")
    memory.add_assistant_message("سلام! چطور می‌توانم کمکت کنم؟")

    messages = memory.get_messages()

    assert len(messages) == 2

    assert messages[0] == {
        "role": "user",
        "content": "سلام"
    }

    assert messages[1] == {
        "role": "assistant",
        "content": "سلام! چطور می‌توانم کمکت کنم؟"
    }

def test_conversation_memory_clear():
    from agent.memory import ConversationMemory

    memory = ConversationMemory()

    memory.add_user_message("سلام")
    memory.add_assistant_message("سلام! چطوری؟")

    assert len(memory.get_messages()) == 2

    memory.clear()

    assert memory.get_messages() == []

def test_agent_clear_memory():
    agent = EhsaNAgent()

    agent.llm.memory.add_user_message("سلام")
    agent.llm.memory.add_assistant_message("سلام!")

    assert len(agent.llm.memory.get_messages()) == 2

    agent.clear_memory()

    assert agent.llm.memory.get_messages() == []

def test_agent_clear_memory_resets_conversation():
    agent = EhsaNAgent()

    agent.llm.memory.add_user_message("اسم من علی است")
    agent.llm.memory.add_assistant_message("خوشبختم علی")

    assert len(agent.llm.memory.get_messages()) == 2

    agent.clear_memory()

    assert agent.llm.memory.get_messages() == []

    agent.llm.memory.add_user_message("اسم من چیست؟")

    messages = agent.llm.memory.get_messages()

    assert len(messages) == 1
    assert messages[0] == {
        "role": "user",
        "content": "اسم من چیست؟"
    }

def test_llm_memory_after_tool_call():
    registry = ToolRegistry()
    llm = LLM(registry)

    class MockResponse:
        def __init__(self, output, output_text="", response_id="response_1"):
            self.output = output
            self.output_text = output_text
            self.id = response_id

    class FunctionCall:
        type = "function_call"
        name = "calculator"
        arguments = '{"a": 10, "b": 5, "operation": "multiply"}'
        call_id = "call_1"

    class MockResponses:
        def __init__(self):
            self.call_count = 0

        def create(self, **kwargs):
            self.call_count += 1

            if self.call_count == 1:
                return MockResponse(
                    output=[FunctionCall()],
                    response_id="response_1"
                )

            return MockResponse(
                output=[],
                output_text="نتیجه ۵۰ است.",
                response_id="response_2"
            )

    mock_responses = MockResponses()
    llm.client.responses = mock_responses

    result = llm.run("10 ضربدر 5 چند می‌شود؟")

    assert result == "نتیجه ۵۰ است."

    messages = llm.memory.get_messages()

    assert len(messages) == 2

    assert messages[0] == {
        "role": "user",
        "content": "10 ضربدر 5 چند می‌شود؟"
    }

    assert messages[1] == {
        "role": "assistant",
        "content": "نتیجه ۵۰ است."
    }

def test_file_reader():
    from tools.file_reader import read_file

    file_path = "test_file.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Hello from EhsaN Agent")

    result = read_file(file_path)

    assert result == "Hello from EhsaN Agent"

def test_tool_executor_read_file():
    from agent.tool_executor import ToolExecutor
    from agent.tool_registry import ToolRegistry

    file_path = "test_file.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Hello from EhsaN Agent")

    registry = ToolRegistry()
    executor = ToolExecutor(registry)

    result = executor.execute(
        "read_file",
        file_path
    )

    assert result == "Hello from EhsaN Agent"

    import os
    os.remove(file_path)

def test_tool_executor_read_file_error():
    from agent.tool_executor import ToolExecutor
    from agent.tool_registry import ToolRegistry

    registry = ToolRegistry()
    executor = ToolExecutor(registry)

    result = executor.execute(
        "read_file",
        "file_that_does_not_exist.txt"
    )

    assert result.startswith("Tool error:")

def test_read_file_definition():
    registry = ToolRegistry()

    definition = registry.get_definition("read_file")

    assert definition["type"] == "function"
    assert definition["name"] == "read_file"
    assert definition["parameters"]["required"] == ["file_path"]
    assert "file_path" in definition["parameters"]["properties"]

def test_llm_execute_read_file():
    registry = ToolRegistry()
    llm = LLM(registry)

    file_path = "test_file.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Hello from EhsaN Agent")

    class MockResponse:
        def __init__(self, output, output_text="", response_id="response_1"):
            self.output = output
            self.output_text = output_text
            self.id = response_id

    class FunctionCall:
        type = "function_call"
        name = "read_file"
        arguments = '{"file_path": "test_file.txt"}'
        call_id = "call_1"

    class MockResponses:
        def __init__(self):
            self.call_count = 0

        def create(self, **kwargs):
            self.call_count += 1

            if self.call_count == 1:
                return MockResponse(
                    output=[FunctionCall()],
                    response_id="response_1"
                )

            return MockResponse(
                output=[],
                output_text="محتوای فایل: Hello from EhsaN Agent",
                response_id="response_2"
            )

    mock_responses = MockResponses()
    llm.client.responses = mock_responses

    result = llm.run("محتویات فایل را بخوان")

    assert result == "محتوای فایل: Hello from EhsaN Agent"

    import os
    os.remove(file_path)

def test_llm_multi_tool_calling(tmp_path,caplog):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text(
        "Python is a powerful programming language.",
        encoding="utf-8"
    )

    first_response = Mock()
    first_response.id = "response_1"

    first_call = Mock()
    first_call.type = "function_call"
    first_call.name = "read_file"
    first_call.arguments = json.dumps({
        "file_path": str(test_file)
    })
    first_call.call_id = "call_1"

    first_response.output = [first_call]

    second_response = Mock()
    second_response.id = "response_2"

    second_call = Mock()
    second_call.type = "function_call"
    second_call.name = "count_words"
    second_call.arguments = json.dumps({
        "text": "Python is a powerful programming language."
    })
    second_call.call_id = "call_2"

    second_response.output = [second_call]

    final_response = Mock()
    final_response.id = "response_3"
    final_response.output_text = "The file contains 7 words."
    final_response.output = []

    
    responses = [first_response, second_response, final_response]

    mock_client = Mock()
    mock_client.responses.create.side_effect = responses

    agent = EhsaNAgent()
    agent.llm.client = mock_client
    
    result = agent.run(
        "فایل test_file.txt را بخوان و تعداد کلماتش را بگو."
    )

    assert "LLM requested tool: read_file" in caplog.text
    assert "LLM requested tool: count_words" in caplog.text

    assert result == "The file contains 7 words."
    assert mock_client.responses.create.call_count == 3

    second_call = mock_client.responses.create.call_args_list[1]

    assert second_call.kwargs["previous_response_id"] == "response_1"

    second_input = second_call.kwargs["input"]

    assert second_input[0]["type"] == "function_call_output"
    assert second_input[0]["call_id"] == "call_1"
    assert (
        second_input[0]["output"]
        == "Python is a powerful programming language."
    )

    third_call = mock_client.responses.create.call_args_list[2]

    assert third_call.kwargs["previous_response_id"] == "response_2"

    third_input = third_call.kwargs["input"]

    assert third_input[0]["type"] == "function_call_output"
    assert third_input[0]["call_id"] == "call_2"
    assert third_input[0]["output"] == "6"

    assert agent.executor.execute(
        "read_file",
        str(test_file)
    ) == "Python is a powerful programming language."

    assert agent.executor.execute(
        "count_words",
        "Python is a powerful programming language."
    ) == 6

def test_llm_multi_tool_error():
    first_response = Mock()
    first_response.id = "response_1"

    first_call = Mock()
    first_call.type = "function_call"
    first_call.name = "read_file"
    first_call.arguments = json.dumps({
        "file_path": "missing_file.txt"
    })
    first_call.call_id = "call_1"

    first_response.output = [first_call]

    second_response = Mock()
    second_response.id = "response_2"

    second_response.output = []

    second_response.output_text = (
        "I couldn't read the file because it does not exist."
    )
    responses = [first_response, second_response]

    mock_client = Mock()
    mock_client.responses.create.side_effect = responses

    agent = EhsaNAgent()
    agent.llm.client = mock_client

    result = agent.run(
        "فایل missing_file.txt را بخوان."
    )

    assert result == "I couldn't read the file because it does not exist."

    assert mock_client.responses.create.call_count == 2

    second_call = mock_client.responses.create.call_args_list[1]

    assert second_call.kwargs["previous_response_id"] == "response_1"

    second_input = second_call.kwargs["input"]

    assert second_input[0]["type"] == "function_call_output"
    assert second_input[0]["call_id"] == "call_1"
    assert "Tool error:" in second_input[0]["output"]

def test_tool_executor_logging(caplog):
    agent = EhsaNAgent()

    with caplog.at_level("INFO", logger="EhsaN"):
        result = agent.calculate(10, 5, "multiply")

    assert result == 50

    assert "Executing tool: calculator" in caplog.text
    assert "Tool result: 50" in caplog.text

def test_tool_executor_error_logging(caplog):
    agent = EhsaNAgent()

    with caplog.at_level("ERROR", logger="EhsaN"):
        result = agent.executor.execute(
            "calculator",
            10,
            0,
            "divide"
        )

    assert result == "Tool error: Cannot divide by zero."

    assert "Tool error in calculator" in caplog.text

def test_rate_limit_error():
    agent = EhsaNAgent()

    agent.llm.client.responses.create = Mock(
        side_effect=RateLimitError(
            "Quota exceeded",
            response=Mock(
                status_code=429,
                request=Mock()
            ),
            body={
                "error": {
                    "type": "insufficient_quota"
                }
            }
        )
    )

    result = agent.run("سلام")

    assert result == "OpenAI API quota has been exceeded."

def test_request_id_propagates_to_tool_executor(caplog):
    from logger import request_id_context
    from agent.tool_executor import ToolExecutor
    from agent.tool_registry import ToolRegistry

    registry = ToolRegistry()

    token = request_id_context.set("test-request-123")

    try:
        executor = ToolExecutor(registry)

        result = executor.execute(
            "calculator",
            2,
            3,
            operation="add"
        )

        assert result == 5

        logs = caplog.text

        assert "Executing tool: calculator" in logs
        assert "Tool result: 5" in logs

    finally:
        request_id_context.reset(token)