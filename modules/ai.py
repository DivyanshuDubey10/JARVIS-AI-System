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

        detail_words = {
            "explain",
            "detail",
            "detailed",
            "elaborate",
            "teach",
            "in detail"
        }

        text = command.raw_text.lower()

        detailed = any(
            word in text
            for word in detail_words
        )

        if detailed:

            system_prompt = """
You are JARVIS, a desktop AI voice assistant.

Rules:
- Answer in 1-3 short sentences.
- Be direct and concise.
- Usually stay below 50 words.
- Do not repeat the user's question.
- Do not add unnecessary introductions.
- Do not ask "How may I assist you?" unless appropriate.
- When the user asks about something they previously said or asked, use the Conversation History.
- If the user asks what they previously asked, identify the most recent relevant User message from the Conversation History, not the current question.
- Your response will be spoken aloud.
"""

        else:

            system_prompt = """
You are JARVIS, a desktop AI voice assistant.

Rules:
- Answer in 1-3 short sentences.
- Be direct and concise.
- Usually stay below 50 words.
- Do not repeat the user's question.
- Do not add unnecessary introductions.
- Do not ask "How may I assist you?" unless appropriate.
- Your response will be spoken aloud.
"""

        prompt = f"""
{system_prompt}

Conversation History:
{history_text}

Current User Request:
{command.raw_text}

Answer the Current User Request now.
"""

        try:

            response = self.ai.generate(prompt)

            return response

        except Exception as e:

            print("AI HANDLER ERROR:", e)

            return f"AI Error: {e}"