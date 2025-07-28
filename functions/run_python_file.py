import os
import subprocess
from functions import config
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the python file specified in the file_path argument with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file to read its contents",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Additional arguments of the python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Argument passed to the python file.",
                ),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory: str, file_path: str, args=[]) -> str:
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    # check that file_path is within working_directory
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    # check that file_path exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    # check that file_path is python file
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    cmd = ["python3", abs_file_path] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=config.TIMEOUT, cwd=abs_working_directory)
        output = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}\n"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

