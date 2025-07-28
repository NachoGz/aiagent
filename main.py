import os
from dotenv import load_dotenv
from google import genai
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment")
    exit(1)

client = genai.Client(api_key=api_key)

system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

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
        genai.types.Content(role="user", parts=[genai.types.Part(text=args.user_prompt)]),
    ]

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=genai.types.GenerateContentConfig(system_instruction=system_prompt)
    )

    print(res.text)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
