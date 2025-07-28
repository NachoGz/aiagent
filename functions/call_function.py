from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google.genai import types
from functions.config import CWD

def call_function(function_call_part: types.FunctionCall, verbose=False) -> types.Content:
    function_call2function = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    function_name = function_call_part.name
    function_args = function_call_part.args or {}

    if function_name is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="unknown_function",
                    response={"error": "Function name is missing"},
                )
            ],
        )

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    try:
        if function_name not in function_call2function:
            response = {"error": f"Unknown function: {function_name}"}
        else:
            function_result = function_call2function[function_name](CWD, **function_args)
            response = {"result": function_result}

    except Exception as e:
        response = {"error": f"Error executing: {e}"}

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response=response,
            )
        ],
    )
