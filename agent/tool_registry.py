from tools.calculator import calculate
from tools.text_tool import count_words
from tools.datetime_tool import get_current_time
from tools.file_reader import read_file


from tools.definitions import (
    calculator_definition,
    count_words_definition,
    get_current_time_definition,
    read_file_definition
    
)


class ToolRegistry:

    def __init__(self):
        self.tools = {
            "calculator": calculate,
            "count_words": count_words,
            "get_current_time": get_current_time,
            "read_file": read_file
            
        }

        self.definitions = {
            "calculator": calculator_definition,
            "count_words": count_words_definition,
            "get_current_time": get_current_time_definition,
            "read_file": read_file_definition
            
        }

    def get(self, tool_name):
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found.")

        return self.tools[tool_name]

    def get_definition(self, tool_name):
        if tool_name not in self.definitions:
            raise ValueError(
                f"Definition for tool '{tool_name}' not found."
            )

        return self.definitions[tool_name]

    def list_tools(self):
        return list(self.tools.keys())

    def list_definitions(self):
        return list(self.definitions.keys())

    def get_all_definitions(self):
        return list(self.definitions.values())