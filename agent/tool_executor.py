from logger import logger
class ToolExecutor:

    def __init__(self, registry):
        self.registry = registry

    def execute(self, tool_name, *args, **kwargs):
        try:
            tool = self.registry.get(tool_name)
            logger.info(f"Executing tool: {tool_name}")

            result = tool(*args, **kwargs)

            logger.info(f"Tool result: {result}")

            return result

        except Exception as e:
            logger.error(f"Tool error in {tool_name}: {e}")
            return f"Tool error: {str(e)}"