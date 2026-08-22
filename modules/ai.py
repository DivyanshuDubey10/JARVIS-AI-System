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

                history_text += (
                    f"{role}: {content}\n"
                )

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

Conversation rules:

- Use Conversation History to understand follow-up questions.
- Treat the current user request as the question you must answer.
- If the user uses words such as "it", "that", "this", "he", "she", "they", "them", "the previous one", or similar references, resolve them using the Conversation History.
- If the user asks a follow-up question, do not assume it is a completely new topic.
- Maintain the topic of the previous conversation when appropriate.
- If the user asks what they previously asked, identify the most recent relevant User message from the Conversation History, not the current request.
- Never answer a previous question instead of the current question.
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