import random

class JarvisAssistant:
    def __init__(self):
        self.conversations = {
            "hello": ["Hello Sir, I am Jarvis.", "Greetings! How can I assist you?", "Hello! Ready for tasks."],
            "bye": ["Goodbye Sir.", "Powering down. Have a nice day.", "See you later!"],
            "how are you": ["I am functioning within normal parameters. Thanks for asking.", "Excellent as always!", "I'm doing well, ready to help."],
            "thanks": ["You're very welcome, Sir.", "My pleasure.", "Don't mention it."]
        }
        self.sorry_responses = ["I'm sorry, that is beyond my current abilities.", "I couldn't quite grasp that command.", "I'm not programmed for that yet."]

    def get_response(self, text):
        """Returns a casual conversational response based on keywords."""
        text = text.lower()
        for key, responses in self.conversations.items():
            if key in text:
                return random.choice(responses)
        return random.choice(self.sorry_responses)
