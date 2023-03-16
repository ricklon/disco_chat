import openai
import json

class AIChatbot:
    def __init__(self, name, bio, model_engine, openai_api_key, prompt=None):
        self.name = name
        self.bio = bio
        self.model_engine = model_engine
        self.prompt = prompt or self.get_default_prompt()
        self.message_history = []
        self.language = "English"
        self.parameters = {}
        self.token_count = 0
        self.active = True

        # Set the OpenAI API key
        self.api_key = openai_api_key
        openai.api_key = self.api_key

    def get_default_prompt(self):
        return f"I am a friendly artificial intelligence ({self.model_engine})."

    def get_response(self, messages):
        if not self.active:
            return "Error: AI is not active."

        # Append the input messages to the message history
        self.message_history.extend(messages)

        # Call the OpenAI API to generate a response
        response = openai.Completion.create(
            engine=self.model_engine,
            prompt=self.message_history,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the generated response and the total number of tokens used
        generated_response = response.choices[0].text
        total_tokens_used = response.total_characters

        # Update the token count for the current conversation
        self.token_count += total_tokens_used

        # Return the generated response and the total number of tokens used
        return generated_response, total_tokens_used

    # Getter and setter methods
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_bio(self):
        return self.bio

    def set_bio(self, bio):
        self.bio = bio

    def get_model_engine(self):
        return self.model_engine

    def set_model_engine(self, model_engine):
        self.model_engine = model_engine

    def get_prompt(self):
        return self.prompt

    def set_prompt(self, prompt):
        self.prompt = prompt

    def get_message_history(self):
        return self.message_history

    def set_message_history(self, history):
        self.message_history = history

    def get_language(self):
        return self.language

    def set_language(self, language):
        self.language = language

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, parameters):
        self.parameters = parameters

    def save_history(self, filename):
        with open(filename, 'w') as f:
            json.dump({'message_history': self.message_history}, f)

    def load_history(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.message_history = data['message_history']

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True
