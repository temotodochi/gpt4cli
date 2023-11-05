# gpt4cli
A small and simple python based CLI app to converse with gpt-4 with contextual history enabled

GPT model can be changed freely from GPT4 to 3.5-turbo or 16k for more memory. GPT4 can get expensive when historical context grows. Very long historical context is useful in personal assistant mode, less useful as programming companion etc. 

Install:

pip install -r requirements.txt

python gpt4cli.py

OR

unzip and run binaries. Windows binary is not code signed, easily causes virus alerts. If there are such issues, you can create your own executables from source with pyinstaller -F gtp4cli.py and whitelist that if you don't trust the binary from here. Linux binary is for AMD64 arch. 

set API keys and default prompt and custom startup instructions during first run.

usage:

Can be run interactively from command line or with command line arguments:

--input INPUT      Use to send GPT4 messages programmatically from command line, exits after response, somewhat pipe friendly output. 

--context CONTEXT  For one-off context switch for the accompanied --input. Will revert to historical context immediately afterwards.  

configuration:

api keys and default context are stored locally in config.ni in plaintext
chat history context is saved in a pickle file context.pkl
