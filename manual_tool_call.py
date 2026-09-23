import json

from dotenv import load_dotenv
from openai import OpenAI

from agent.tool_registry import ToolRegistry
from agent.tool_executor import ToolExecutor


load_dotenv()

client = OpenAI()

registry = ToolRegistry()
executor = ToolExecutor(registry)

tools = [
    registry.get_definition("calculator")
]

user_input = (
    "برای پاسخ به این درخواست حتماً از ابزار calculator استفاده کن: "
    "حاصل 25 ضربدر 4 را حساب کن."
)

response = client.responses.create(
    model="gpt-5.6-luna",
    input=user_input,
    tools=tools,
    tool_choice="required"
)

for item in response.output:

    if item.type == "function_call":

        print("Tool selected:", item.name)
        print("Arguments:", item.arguments)

        arguments = json.loads(item.arguments)

        result = executor.execute(
            item.name,
            arguments["a"],
            arguments["b"],
            arguments["operation"]
        )
        

        print("Tool result:", result)

        response = client.responses.create(
         model="gpt-5.6-luna",
         input=[
            {
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": str(result)
            }
        ],
        previous_response_id=response.id,
    )

    print("Final answer:", response.output_text)