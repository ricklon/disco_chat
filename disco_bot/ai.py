import openai
import json

class AI:
    def __init__(self, name, model_engine, openai_api_key, prompt=None):
        self.name = name
        self.model_engine = model_engine
        self.prompt = prompt or self.get_default_prompt()
        self.conversation_history = self.prompt + '\n'
        self.active = True

        # Set the OpenAI API key
        self.api_key = openai_api_key
        openai.api_key = self.api_key

    def get_default_prompt(self):
        return f"I am a friendly artificial intelligence ({self.model_engine})."

def get_response(self, message):
    if not self.active:
        return "Error: AI is not active."
    self.conversation_history += f"{self.name}: {message}\n"
    prompt = self.conversation_history
    completions = openai.Completion.create(
        engine=self.model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.7,
    )
    response = completions.choices[0].text
    self.conversation_history += f"{self.name}: {response}\n"
    return f"{self.name}: {response}"



    def set_prompt(self, prompt):
        self.prompt = prompt

    def get_prompt(self):
        return self.prompt

    def save_conversation_history(self, file_name):
        with open(file_name, 'w') as f:
            json.dump({'conversation_history': self.conversation_history}, f)

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True
