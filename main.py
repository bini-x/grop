import os, json, sys

from dotenv import load_dotenv
from openai import OpenAI
from argparse import ArgumentParser
from openai.types.chat import ChatCompletionMessageParam
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("API key was not found!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]


for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    message = response.choices[0].message

    if message.tool_calls:
        messages.append(message)
        for t in message.tool_calls:
            result_message = call_function(t, verbose=args.verbose)
            if result_message["content"] == "":
                raise Exception("No content")
            messages.append(result_message)
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(message.content)
        break

    if response.usage is not None and args.verbose:
        print(f"User prompt: {args.user_prompt}")

        print("Prompt tokens: ", response.usage.prompt_tokens)
        print("Response tokens: ", response.usage.completion_tokens)
else:
    print("Maximum iterations reached. The agent did not produce a final response.")
    sys.exit(1)
