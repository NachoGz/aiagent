import os
from dotenv import load_dotenv
from google.genai import types
from google import genai
import argparse
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment")
    exit(1)

client = genai.Client(api_key=api_key)

system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- List files and directories
- Read file contents
- Execute Python files with optional arguments, if these are not provided there is no need to ask for them. Their absence implies that the user doesn't want to use them. DO NOT ASK THE USER TO PROVIDE ARGUMENTS
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
DO NOT RESPOND UNLESS YOU HAVE THE ANSWER TO THE REQUEST. THERE IS NO NEED TO TELL THE USER WHAT YOU ARE DOING.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def main():
    # define cli arguments
    parser = argparse.ArgumentParser(
        prog="aiagent",
        description="a simple cli tool for interacting with Google's Gemini",
    )

    parser.add_argument("user_prompt", help="The prompt/question to send to Gemini")
    parser.add_argument("-v" ,"--verbose", action="store_true", help="Show detailed information (prompt, token counts)")
    args = parser.parse_args()

    # list for storing past prompts for memory purposes
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]

    for i in range(20):
        try:
            res = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions]
                )
            )

        except Exception as e:
            print(f"Error executing generate_content: {e}")
            exit(1)

        if res.text:
            print(f"Final response: {res.text}")
            break

        if res.candidates:
            for candidate in res.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            if res.usage_metadata is not None:
                print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {res.usage_metadata.candidates_token_count}")

        if res.function_calls:
            for function_call_part in res.function_calls:
                function_call_result = call_function(function_call_part, args.verbose)
                messages.append(function_call_result)
                if args.verbose:
                    if (function_call_result.parts and
                            function_call_result.parts[0].function_response):
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    else:
                        print(f"-> Function call completed (no response data)")

if __name__ == "__main__":
    main()
