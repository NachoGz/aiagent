from functions import config
import os

def get_file_content(working_directory: str, file_path: str) -> str:
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    # check that file_path is inside the working_directory
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    # check that file_path is a file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path, "r") as f:
            content = f.read()
            if len(content) > config.MAX_CHARS:
                # truncate in memory plus truncation message
                truncated_content = content[:config.MAX_CHARS] + f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'

                # replace the original content with the truncated version
                with open(abs_file_path, "w") as f:
                    f.write(truncated_content)

                return truncated_content

        return content
    except Exception as e:
        return f'Error opening file: {e}'

