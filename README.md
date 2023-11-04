# gpt4cli
A small and simple python based CLI app to converse with gpt-4 with contextual history enabled

Install:

unzip and run to set API keys and default prompt and custom startup instructions. 

usage:

Can be run interactively from command line or with command line arguments:

--input INPUT      Use to send GPT4 messages programmatically from command line, exits after response, somewhat pipe friendly output. 

--context CONTEXT  Use to set temporary one-use context for special prompts, only used for --input sent with it.

configuration:

api keys and default context are stored locally in config.ni in plaintext
chat history context is saved in a pickle file context.pkl
