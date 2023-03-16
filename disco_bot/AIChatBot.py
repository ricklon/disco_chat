import openai
import json

class AIChatbot:
    def __init__(self, name, bio, model, openai_api_key, system_message=None):
        self.name = name
        self.bio = bio
        self.token_count = 0
        self.message_history = []
        self.model = model
        self.language = "English"
        self.parameters = {}
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key

        # Define knowledge_cutoff and current_date
        knowledge_cutoff = "2021-09"
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        self.system_message = system_message or [
            {
                "role": "system",
                "content": f"You are {self.name}, an AI chatbot. Knowledge cutoff: {knowledge_cutoff}. Current date: {current_date}."
            }
        ]
        # Initialize the message_history as an empty list of dictionaries
        self.message_history = []


    def get_default_prompt(self):
        return f"I am a friendly artificial intelligence ({self.model_engine})."

    def get_response(self, messages):
        """Returns the response for the given prompt using the OpenAI API."""
        # Append the input messages to the message history
        self.message_history.extend(messages)

        chat_messages = [{"role": "system", "content": self.system_message}]
        for message in self.message_history:
            chat_messages.append({"role": "user", "content": message})

        # Call the OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model=self.model_engine,
            messages=chat_messages,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the generated response, the total number of tokens used, and the finish_reason
        generated_response = response.choices[0].message["content"]
        total_tokens_used = response.usage["total_tokens"]
        finish_reason = response.choices[0].finish_reason

        # Update the token count for the current conversation
        self.token_count += total_tokens_used

        # Return the generated response, the total number of tokens used, and the finish_reason
        return generated_response, total_tokens_used, finish_reason

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
