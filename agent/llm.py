import json
import os

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

from agent.tool_executor import ToolExecutor
from agent.memory import ConversationMemory
from logger import logger


load_dotenv()


class OfflineResponses:
    def create(self, **kwargs):
        raise RuntimeError(
            "OpenAI API client is not configured."
        )


class OfflineClient:
    def __init__(self):
        self.responses = OfflineResponses()


class LLM:

    def __init__(self, registry):
        if os.getenv("OPENAI_API_KEY"):
            self.client = OpenAI()
        else:
            self.client = OfflineClient()

        self.model = "gpt-5.6-luna"
        self.registry = registry
        self.executor = ToolExecutor(registry)
        self.memory = ConversationMemory()

    def _get_tools(self):
        tools = self.registry.get_all_definitions()

        tools.append({
            "type": "web_search"
        })

        return tools

    def run(self, user_input):
        logger.info("LLM request started.")

        self.memory.add_user_message(user_input)

        tools = self._get_tools()

        if isinstance(self.client, OfflineClient):
            logger.error("OpenAI API key is not configured.")
            return "OpenAI API key is not configured."

        try:
            response = self.client.responses.create(
                model=self.model,
                input=self.memory.get_messages(),
                tools=tools
            )
        except RateLimitError:
            logger.error("OpenAI API quota exceeded.")
            return "OpenAI API quota has been exceeded."

        while True:

            for item in response.output:

                if item.type == "function_call":

                    arguments = json.loads(item.arguments)

                    logger.info(
                        f"LLM requested tool: {item.name}"
                    )

                    result = self._execute_tool(
                        item.name,
                        arguments
                    )

                    response = self.client.responses.create(
                        model=self.model,
                        input=[
                            {
                                "type": "function_call_output",
                                "call_id": item.call_id,
                                "output": str(result)
                            }
                        ],
                        previous_response_id=response.id,
                    )

                    break

            else:
                answer = response.output_text

                logger.info("LLM response received.")

                self.memory.add_assistant_message(answer)

                return answer

    def _execute_tool(self, tool_name, arguments):

        return self.executor.execute(
            tool_name,
            **arguments
        )