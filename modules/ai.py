import os
from dotenv import load_dotenv
from core.ai_service import AIService

load_dotenv()


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

        detail_words = {
            "explain",
            "detail",
            "detailed",
            "elaborate",
            "teach",
            "in detail",
            "teach me",
            "explain in detail"
        }

        detailed = any(
            word in command.raw_text.lower()
            for word in detail_words
        )

        if detailed:
            system_prompt = """
        You are JARVIS.

        The user has asked for a detailed explanation.

        Give a complete explanation.
        Use examples if appropriate.
        """
        else:
            system_prompt = """
You are JARVIS, a desktop AI voice assistant.

Rules:
- Answer in 2-3 short sentences.
- Be direct and concise.
- Avoid unnecessary introductions.
- Your response will be spoken aloud.
"""

        prompt = f"""
{system_prompt}

Conversation History:
{history_text}

User: {command.raw_text}
"""

        try:
            response = self.ai.generate(prompt)

            return response
        
        except Exception as e:
            return f"AI Error: {e}"