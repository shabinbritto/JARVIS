
from ai.llm import AIGateway


class Jarvis:

    def __init__(self):
        self.name = "Jarvis"
        self.ai_gateway = AIGateway()

    def process(self, user_input):
        user_input = user_input.strip()

        if not user_input:
            return "Please type something."

        message = user_input.lower()

        if message == "hello":
            return "Hello! I am Jarvis. How can I help you?"

        if message == "who are you":
            return "I am Jarvis, your personal AI assistant."

        if message == "what can you do":
            return (
                "I will help you with AI, studying, planning, "
                "memory, documents, voice and other tasks."
            )

        return (
            "I received your message, but AI is not available yet. "
            "No data was sent."
        )
