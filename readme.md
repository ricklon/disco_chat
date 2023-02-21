# Discord AI Chatbot Manager

This is a Python script that allows you to manage a group of AI chatbots on a Discord server. With this script, you can create new AIs, activate and deactivate them, rename them, and set their conversation history and prompt. You can also get the original prompt, list all the available AIs, and save the entire conversation history for an AI as a JSON file. 

To use the script, you need to have a Discord bot token and an OpenAI API key. Once you have those, you can run the script and interact with the AIs using the following commands:

- **Talk to an AI:** `!talk [ai name] [message]`
- **Create a new AI:** `!create [ai name] [model engine]`
- **Rename an AI:** `!rename [old name] [new name]`
- **Set the conversation history:** `!sethistory [ai name] [file name]`
- **List all AIs:** `!listais`
- **Deactivate an AI:** `!deactivate [ai name]`
- **Activate an AI:** `!activate [ai name]`
- **Remove an AI:** `!remove [ai name]`
- **Set the AI model:** `!setmodel [ai name] [model engine]`
- **Get the original prompt:** `!getprompt [ai name]`
- **Set a new prompt:** `!setprompt [ai name] [prompt]`
- **Save the entire conversation history as JSON:** `!savehistory [ai name] [file name]`
