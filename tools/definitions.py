calculator_definition = {
    "type": "function",
    "name": "calculator",
    "description": "Perform a mathematical calculation.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "First number."
            },
            "b": {
                "type": "number",
                "description": "Second number."
            },
            "operation": {
                "type": "string",
                "enum": [
                    "add",
                    "subtract",
                    "multiply",
                    "divide"
                ],
                "description": "The mathematical operation to perform."
            }
        },
        "required": [
            "a",
            "b",
            "operation"
        ],
        "additionalProperties": False
    },
    "strict": True
}


count_words_definition = {
    "type": "function",
    "name": "count_words",
    "description": "Count the number of words in a text.",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The text to count words in."
            }
        },
        "required": [
            "text"
        ],
        "additionalProperties": False
    },
    "strict": True
}

get_current_time_definition = {
    "type": "function",
    "name": "get_current_time",
    "description": "Get the current local time.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    },
    "strict": True
}

web_search_definition = {
    "type": "function",
    "name": "web_search",
    "description": "Search the web for information.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query."
            }
        },
        "required": [
            "query"
        ],
        "additionalProperties": False
    },
    "strict": True
}

read_file_definition = {
    "type": "function",
    "name": "read_file",
    "description": "Read the contents of a text file.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path of the text file to read."
            }
        },
        "required": [
            "file_path"
        ],
        "additionalProperties": False
    },
    "strict": True
}