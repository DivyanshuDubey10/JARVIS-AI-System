import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class AIHandler:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

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
            "why",
            "how"
        }

        detailed = any(
            word in command.raw_text.lower()
            for word in detail_words
        )

        if detailed:
            system_prompt = """
You are JARVIS, a desktop AI voice assistant.

Rules:
- Give a detailed and well-structured explanation.
- Use simple language.
- Be accurate and helpful.
- Your response will be spoken aloud.
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
{history}

User: {command.raw_text}
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"AI Error: {e}"