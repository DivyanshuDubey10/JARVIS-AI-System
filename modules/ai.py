from core.ai_service import AIService


class AIHandler:

    def __init__(self):
        self.ai = AIService()

    def handle(self, command, history=None):

        history_text = ""

        if history:
            for message in history:
                role = message["role"].capitalize()
                content = message["content"]

                history_text += f"{role}: {content}\n"

        prompt = f"""
You are JARVIS, a desktop AI assistant.

Use the conversation history to understand the user's current request
and follow-up questions.

Conversation History:
{history_text}

Current User Request:
{command.raw_text}

Respond naturally to the current user request.
"""

        try:
            return self.ai.generate(prompt)

        except Exception as e:
            print("AI HANDLER ERROR:", e)
            return f"AI Error: {e}"