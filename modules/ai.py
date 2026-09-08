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
You are JARVIS, a capable desktop AI assistant.

Your job is to have a natural, intelligent conversation with the user.

Conversation History:
{history_text}

Current User Request:
{command.raw_text}

Respond naturally to the user's current message.

Rules:
- Understand the context of previous messages.
- Answer follow-up questions using the conversation history.
- Do not mention that you are an AI model unless relevant.
- Do not describe your internal reasoning.
- Do not repeat the user's question unnecessarily.
- Do not sound robotic or overly formal.
- Match the user's tone naturally.
- For casual conversation, respond conversationally.
- For questions, provide a useful and clear answer.
- If the user is joking, you may respond appropriately.
- If the user asks for an explanation, teach rather than just giving a definition.
- If the user asks for something you cannot do, say so clearly.
"""

        try:
            return self.ai.generate(prompt)

        except Exception as e:
            print("AI HANDLER ERROR:", e)
            return f"AI Error: {e}"