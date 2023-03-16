class AIChatbotManager:
    def __init__(self, openai_api_key):
        self.bots = {}
        self.openai_api_key = openai_api_key

    def create_bot(self, name, bio, model_engine="davinci", initial_prompt="Hello, how can I help you?", language="English", parameters=None):
        bot = AIChatbot(name, bio, model_engine, self.openai_api_key)
        bot.set_prompt(initial_prompt)
        bot.set_language(language)
        if parameters:
            bot.set_parameters(parameters)
        self.bots[name] = bot
        return bot

    def delete_bot(self, name):
        del self.bots[name]

    def get_bot(self, name):
        return self.bots.get(name)

    def get_all_bots(self):
        return self.bots

    def assign_bot(self, name, user_or_channel):
        bot = self.get_bot(name)
        bot.set_message_history([])  # Initialize message history to empty list
        # Use the Slack API to initiate a direct message conversation between
        # the bot and the user or channel
        pass

    def unassign_bot(self, name, user_or_channel):
        bot = self.get_bot(name)
        # Use the Slack API to end the direct message conversation between
        # the bot and the user or channel
        pass
