class Jarvis:

    def __init__(self):
        self.name = "Jarvis"

    def process(self, user_input):
        user_input = user_input.strip()

        if not user_input:
            return "Please type something."

        if user_input.lower() == "hello":
            return "Hello! I am Jarvis. How can I help you?"

        if user_input.lower() == "who are you":
            return "I am Jarvis, your personal AI assistant."

        if user_input.lower() == "what can you do":
            return "I will help you with AI, studying, planning, memory, documents, voice and other tasks."

        return f"I received your message: {user_input}"