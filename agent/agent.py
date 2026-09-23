from agent.llm import LLM
from agent.tool_executor import ToolExecutor
from agent.tool_registry import ToolRegistry
from logger import logger


class EhsaNAgent:

    def __init__(self):
        self.name = "EhsaN"

        self.registry = ToolRegistry()

        self.tools = self.registry.tools

        self.executor = ToolExecutor(self.registry)

        self.llm = LLM(self.registry)

    def calculate(self, a, b, operation):
        return self.executor.execute(
            "calculator",
            a,
            b,
            operation
        )

    def count_words(self, text):
        return self.executor.execute(
            "count_words",
            text
        )

    def get_tool_definitions(self):
        return self.registry.get_all_definitions()

    def run(self, user_input):
        logger.info("Agent started.")

        result = self.llm.run(user_input)

        logger.info("Agent finished.")

        return result
    def clear_memory(self):
        self.llm.memory.clear()