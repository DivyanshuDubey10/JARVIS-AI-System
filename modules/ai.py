
from core.ai_service import AIService
from core.persistent_memory import PersistentMemory


class AIHandler:

    def __init__(self):
        self.ai = AIService()
        self.memory = PersistentMemory()

        self.memory_categories = {
            "current_project": [
                "current project",
                "project",
            ],
            "preferred_language": [
                "preferred language",
                "programming language",
                "favourite language",
                "favorite language",
            ],
            "college": [
                "college",
                "university",
            ],
            "response_preference": [
                "response preference",
                "answer preference",
                "answer style",
            ],
            "operating_system": [
                "operating system",
                "os",
            ],
        }

    def identify_category(self, text):

        text = text.lower()

        for key, phrases in self.memory_categories.items():
            for phrase in phrases:
                if phrase in text:
                    return key

        return None

    def handle(self, command, history=None):

        raw_text = command.raw_text.strip()
        text = raw_text.lower().rstrip(" .?!")

        # --------------------------------
        # REMEMBER / UPDATE
        # --------------------------------

        prefixes = [
            "remember that ",
            "remember ",
            "save that ",
            "save ",
            "my ",
        ]

        for prefix in prefixes:

            if not text.startswith(prefix):
                continue

            fact = raw_text[len(prefix):].strip()

            category = self.identify_category(fact)

            if category and " is " in fact.lower():

                value = fact.split(" is ", 1)[1].strip().rstrip(".!?")

                if value:
                    self.memory.remember(category, value)

                    return (
                        f"I've saved your {category.replace('_', ' ')} "
                        f"as {value}."
                    )

        # --------------------------------
        # RECALL ALL MEMORIES
        # --------------------------------

        recall_phrases = [
            "what do you remember",
            "show my memories",
            "list my memories",
        ]

        if any(phrase in text for phrase in recall_phrases):

            memories = self.memory.get_all()

            if not memories:
                return "I don't have any saved memories yet."

            return "Here is what I remember: " + "; ".join(
                f"{key.replace('_', ' ')}: {value}"
                for key, value in memories.items()
            )

        # --------------------------------
        # RECALL SPECIFIC MEMORY
        # --------------------------------

        if text.startswith(("what is my ", "what's my ", "tell me my ")):

            category = self.identify_category(text)

            if category:
                value = self.memory.recall(category)

                if value:
                    return f"Your {category.replace('_', ' ')} is {value}."

                return f"I don't have your {category.replace('_', ' ')} saved."

        # --------------------------------
        # FORGET MEMORY
        # --------------------------------

        forget_prefixes = [
            "forget ",
            "delete memory ",
            "remove memory ",
        ]

        for prefix in forget_prefixes:

            if text.startswith(prefix):

                category = self.identify_category(
                    text[len(prefix):]
                )

                if category and self.memory.forget(category):
                    return (
                        f"I've forgotten your "
                        f"{category.replace('_', ' ')}."
                    )

                return "I couldn't find that saved memory."

        # --------------------------------
        # NORMAL AI CONVERSATION
        # --------------------------------

        history_text = ""

        if history:
            history_text = "\n".join(
                f"{message['role'].capitalize()}: {message['content']}"
                for message in history
            )

        memories = self.memory.get_all()

        memory_text = "\n".join(
            f"- {key}: {value}"
            for key, value in memories.items()
        ) or "No saved memories."

        prompt = f"""
You are JARVIS, a capable desktop AI assistant.

Saved memories:
{memory_text}

Conversation history:
{history_text}

Current user request:
{raw_text}

Use relevant saved memories when responding.
Do not contradict saved facts without new information.
Respond naturally and concisely.
"""

        try:
            return self.ai.generate(prompt)

        except Exception as e:
            print("AI HANDLER ERROR:", e)
            return f"AI Error: {e}"
