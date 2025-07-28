import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file in the file_path arguments with the content argument",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file to write the content",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text to be written to the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.join(abs_working_directory, file_path)

    # check that file_path is within working_directory
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        dirname = os.path.dirname(abs_file_path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing content to "{file_path}": {e}'
