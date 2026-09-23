from unittest.mock import Mock

from evaluation.evaluator import Evaluator


def test_evaluator_pass():
    agent = Mock()

    agent.run.return_value = "50"

    evaluator = Evaluator(agent)

    result = evaluator.run_case(
        "10 ضربدر 5 چند میشه؟",
        "50"
    )

    assert result["input"] == "10 ضربدر 5 چند میشه؟"
    assert result["expected"] == "50"
    assert result["actual"] == "50"
    assert result["passed"] is True

def test_evaluator_fail():
    agent = Mock()

    agent.run.return_value = "40"

    evaluator = Evaluator(agent)

    result = evaluator.run_case(
        "10 ضربدر 5 چند میشه؟",
        "50"
    )

    assert result["actual"] == "40"
    assert result["expected"] == "50"
    assert result["passed"] is False

def test_evaluator_run_all():
    agent = Mock()

    agent.run.side_effect = [
        "50",
        "50"
    ]

    evaluator = Evaluator(agent)

    cases = [
        {
            "name": "multiply",
            "input": "10 ضربدر 5 چند میشه؟",
            "expected": "50"
        },
        {
            "name": "add",
            "input": "20 به علاوه 30 چند میشه؟",
            "expected": "50"
        }
    ]

    results = evaluator.run_all(cases)

    assert len(results) == 2
    assert results[0]["passed"] is True
    assert results[1]["passed"] is True
    assert agent.run.call_count == 2

def test_calculate_score():
    agent = Mock()

    evaluator = Evaluator(agent)

    results = [
        {"passed": True},
        {"passed": True},
        {"passed": False},
        {"passed": True},
    ]

    score = evaluator.calculate_score(results)

    assert score == 0.75

def test_generate_report():
    agent = Mock()

    evaluator = Evaluator(agent)

    results = [
        {"passed": True},
        {"passed": True},
        {"passed": False},
        {"passed": True},
    ]

    report = evaluator.generate_report(results)

    assert report["total"] == 4
    assert report["passed"] == 3
    assert report["failed"] == 1
    assert report["score"] == 0.75

from agent.agent import EhsaNAgent


def test_real_agent_evaluation():
    agent = EhsaNAgent()

    agent.llm.client = Mock()

    response = Mock()
    response.output_text = "50"
    response.output = []

    agent.llm.client.responses.create.return_value = response

    evaluator = Evaluator(agent)

    result = evaluator.run_case(
        "10 ضربدر 5 چند میشه؟",
        "50"
    )

    assert result["passed"] is True

def test_real_agent_evaluation_fail():
    agent = Mock()
    agent.run.return_value = "40"

    evaluator = Evaluator(agent)

    result = evaluator.run_case(
        "10 ضربدر 5 چند میشه؟",
        "50"
    )

    assert result["passed"] is False
    assert result["actual"] == "40"
    assert result["expected"] == "50"

def test_real_file_reader():
    from agent.agent import EhsaNAgent

    agent = EhsaNAgent()

    result = agent.executor.execute(
        "read_file",
        "test.txt"
    )

    assert result == "Python is a powerful programming language."

def test_real_agent_multi_tool_evaluation(tmp_path):
    from unittest.mock import Mock
    from agent.agent import EhsaNAgent

    test_file = tmp_path / "test_file.txt"

    test_file.write_text(
        "Python is a powerful programming language.",
        encoding="utf-8"
    )

    agent = EhsaNAgent()

    first_response = Mock()
    first_response.id = "response_1"

    first_call = Mock()
    first_call.type = "function_call"
    first_call.name = "read_file"
    first_call.arguments = (
        '{"file_path": "' + str(test_file).replace("\\", "\\\\") + '"}'
    )
    first_call.call_id = "call_1"

    first_response.output = [first_call]

    second_response = Mock()
    second_response.id = "response_2"

    second_call = Mock()
    second_call.type = "function_call"
    second_call.name = "count_words"
    second_call.arguments = (
        '{"text": "Python is a powerful programming language."}'
    )
    second_call.call_id = "call_2"

    second_response.output = [second_call]

    final_response = Mock()
    final_response.output = []
    final_response.output_text = "The file contains 6 words."

    mock_client = Mock()

    mock_client.responses.create.side_effect = [
        first_response,
        second_response,
        final_response
    ]

    agent.llm.client = mock_client

    evaluator = Evaluator(agent)

    result = evaluator.run_case(
        "فایل را بخوان و تعداد کلماتش را بگو.",
        "The file contains 6 words."
    )

    assert result["passed"] is True

    assert mock_client.responses.create.call_count == 3

    second_request = mock_client.responses.create.call_args_list[1]

    assert second_request.kwargs["previous_response_id"] == "response_1"

    third_request = mock_client.responses.create.call_args_list[2]

    assert third_request.kwargs["previous_response_id"] == "response_2"

def test_real_agent_file_not_found_evaluation():
    from agent.agent import EhsaNAgent

    agent = EhsaNAgent()

    first_response = Mock()
    first_response.id = "response_1"

    first_call = Mock()
    first_call.type = "function_call"
    first_call.name = "read_file"
    first_call.arguments = (
        '{"file_path": "this_file_does_not_exist.txt"}'
    )
    first_call.call_id = "call_1"

    first_response.output = [first_call]

    final_response = Mock()
    final_response.output = []
    final_response.output_text = (
        "I couldn't read the file because it does not exist."
    )

    mock_client = Mock()

    mock_client.responses.create.side_effect = [
        first_response,
        final_response
    ]

    agent.llm.client = mock_client

    evaluator = Evaluator(agent)

    result = evaluator.run_case(
        "این فایل را بخوان.",
        "I couldn't read the file because it does not exist."
    )

    assert result["passed"] is True

    assert mock_client.responses.create.call_count == 2

    second_request = mock_client.responses.create.call_args_list[1]

    assert second_request.kwargs["previous_response_id"] == "response_1"

    tool_output = second_request.kwargs["input"][0]["output"]

    assert "Tool error:" in tool_output

def test_generate_category_report():
    agent = Mock()
    evaluator = Evaluator(agent)

    results = [
        {
            "passed": True,
            "category": "calculator"
        },
        {
            "passed": True,
            "category": "calculator"
        },
        {
            "passed": False,
            "category": "calculator"
        },
        {
            "passed": True,
            "category": "file_reader"
        }
    ]

    report = evaluator.generate_category_report(results)

    assert report["calculator"]["total"] == 3
    assert report["calculator"]["passed"] == 2
    assert report["calculator"]["failed"] == 1
    assert report["calculator"]["score"] == 2 / 3

    assert report["file_reader"]["total"] == 1
    assert report["file_reader"]["passed"] == 1
    assert report["file_reader"]["failed"] == 0
    assert report["file_reader"]["score"] == 1.0