from openai import OpenAI
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import ANSI
from colorama import Fore, Style, init
init(autoreset=True) # Automatically reset colorama color after each print statement

import json
import pickle
import argparse
import configparser
import os

# Custom keybind for multiline entry
bindings = KeyBindings()

@bindings.add('enter')
def _(event):
    " When enter is pressed, send the text. "
    event.current_buffer.validate_and_handle()

@bindings.add('c-j')
def _(event):
    " When control+enter is pressed, insert a newline. "
    event.current_buffer.insert_text('\n')

# Create a PromptSession with the custom key bindings
session = PromptSession(key_bindings=bindings)


def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        config['Settings'] = {
            'api_key': input("Enter your OpenAI API key: "),
            'default_context': input("Context is king! Your context will be saved in a context file, but for a start, tell in a few sentences to gpt about yourself and in which manner you would like it to respond to you.\n\nFor example: I'm a techie from $city and $country, as european i'd like more direct answers than americans and i'm well versed in $expertise and don't need beginner warnings in that field. You will work as my personal assistant. Lets assume we are polite to each others even when we don't write in that manner. \n\nYou can input widely different contexts here, for examples check out https://github.com/f/awesome-chatgpt-prompts \n\nEnter your default context: ")
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        config.read('config.ini')

    return config['Settings']['api_key'], config['Settings']['default_context']

api_key, default_context = load_config()
client = OpenAI(api_key=api_key)


def save_context_to_disk(context):
    with open('context.pkl', 'wb') as f:
        pickle.dump(context, f)

def load_context_from_disk():
    try:
        with open('context.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []  # or return an empty dict or your default context

def generate_response(prompt, context):
    """
    Generates a response using the GPT-4 model based on the given prompt and context.

    Parameters:
    - prompt (str): The user's input.
    - context (list): The conversation history.

    Returns:
    - str: The generated response.
    """
    # Prepare the messages for the API call
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.extend(context)  # Include the conversation history
    messages.append({"role": "user", "content": prompt})  # Add the current user input

    # Call the GPT-3.5-turbo model
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    # Convert the response object to a dictionary
    completion_dict = completion.model_dump()
    # Extracting the generated text from the response
    generated_text = completion_dict['choices'][0]['message']['content'].strip()

    return generated_text


def main():
    parser = argparse.ArgumentParser(description='Interact with GPT-4. Email: mikael@levoniemi.com')
    parser.add_argument('--input', default='', help='The user input.')
    parser.add_argument('--context', default=None, help='Override saved context for one time prompts etc')
    args = parser.parse_args()

    context = load_context_from_disk()
    if context is None:
        context = [default_context]

    if args.context is not None:  # If --context argument is provided
        context = [{"role": "user", "content": args.context}]

    if args.input:  # If input argument is provided, process it first
        user_input = args.input
        context.append({"role": "user", "content": user_input})  # Add user message to context
        try:
            response = generate_response(user_input, context)  # Generate response with updated context
        except Exception as e:
            print(f"Error: {e}")
            return
        response = response.replace("\n", " ")
        print(f'GPT-4: {response}') # Replacing newlines with spaces
        context.append({"role": "assistant", "content": response})
    else:
        print(f"\nEnter to send, ctrl-enter for newline, type exit to quit.\n")
        while True:
            user_input = session.prompt(ANSI('\x1b[32mYou:\x1b[0m '), multiline=True)  # Collect user input
            if user_input.lower() == 'exit':  # Exit condition
                break

            context.append({"role": "user", "content": user_input})

            try:
                response = generate_response(user_input, context)
            except Exception as e:
                print(f"Error: {e}")
                continue

            print(f'{Fore.RED}GPT-4:{Style.RESET_ALL} {response}', end='\n\n')
            context.append({"role": "assistant", "content": response})

            save_context_to_disk(context)
if __name__ == "__main__":
    main()
