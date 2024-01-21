from dotenv import load_dotenv
import os
import argparse

import subprocess
import requests
import json

# ! PARAMA
env_filename = ".env"
env_key_name = "OPENAI_KEY"

system_prompt = (
    "system: You are being run in a scaffold in a shell on a Macbook. When you want to run a "
    "shell command, write it in a <bash> XML tag. You will be shown the result of the command "
    "and be able to run more commands. Other things you say will be sent to the user. When you "
    "come to know how to do something, don't explain how to do it, just start doing it by emitting "
    "bash commands one at a time. The user uses fish, but you're in a bash shell. Remember that you "
    "can't interact with stdin directly, so if you want to e.g. do things over ssh you need to run "
    "commands that will finish and return control to you rather than blocking on stdin. Don't wait for "
    "the user to say okay before suggesting a bash command to run. Do NOT include your explanation, "
    "just say the command itself.\n\n"
    "If you can't do something without assistance, please suggest a way of doing it without assistance anyway.\n\n"
    "Just do not output any explanation, only the command. Make sure to never write an explanation before the command, just write the command that will be implemented."
    "Only ever output one single bash command, nothing else."
)

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.strip()
    

def stream_gpt_response(OPENAI_KEY, user_input, temperature=0):
    prompt_to_send = system_prompt + user_input
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,   
        "max_tokens": 100,
        "temperature": temperature
    }

    stream_url = "https://api.openai.com/v1/chat/completions"
    buffer = ""
    with requests.post(stream_url, headers=headers, json=data, stream=True) as r:
        if r.encoding is None:
            r.encoding = 'utf-8'
        for line in r.iter_lines(decode_unicode=True):
            buffer += line
            try:
                json_response = json.loads(buffer)
                if 'choices' in json_response and json_response['choices']:
                    text = json_response['choices'][0].get('message', {}).get('content', '')
                    print(text, end='', flush=True)
                    buffer = ""   
                else:
                    print(f"Unexpected response format: {buffer}")
                    buffer = ""   
            except json.JSONDecodeError:
                continue   

    return buffer.strip()

def set_api_key(api_key):
    # Construct the path to the .env file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    env_path = os.path.join(parent_dir, env_filename)

    with open(env_path, 'w') as f:
        f.write(f"OPENAI_KEY={api_key}\n")
    print(f"API Key set and saved in {env_path}")


def main():
    parser = argparse.ArgumentParser(description='GPT-CLI Application')
    parser.add_argument('--key', help='Set the OpenAI API key', type=str)

    args = parser.parse_args()

    if args.key:
        print("HELLOOOO")
        set_api_key(args.key)
    else:
        # Load environment variables from .env file

        # Construct the path to the .env file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        env_path = os.path.join(parent_dir, env_filename)

        load_dotenv(env_path)
        OPENAI_KEY = os.getenv(env_key_name)
        if OPENAI_KEY is None:
            raise ValueError(f"API key not found in. Ensure that API key is set.")

        # ... rest of your main function logic ...
        while True:
            user_input = input("query> ")
            if user_input.lower() == 'exit':
                break

            streamed_output = stream_gpt_response(OPENAI_KEY, user_input, temperature=0)

            if "<bash>" in streamed_output:
                command_to_run = streamed_output.strip("<bash>").strip("</bash>").strip()
                print(f"output: {command_to_run}")
                approval = input("should I run this command? (y/n): ")
                if approval.lower() == 'y':
                    output = run_command(command_to_run)
                    print(f"output: \n{output}\n")


if __name__ == "__main__":
    main()