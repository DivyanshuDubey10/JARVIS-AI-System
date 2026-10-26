
from core.ai_service import AIService
from core.persistent_memory import PersistentMemory


class AIHandler:

    def __init__(self):
        self.ai = AIService()
        self.memory = PersistentMemory()

    def handle(self, command, history=None):
        raw_text = command.raw_text.strip()
        text = raw_text.lower().rstrip(" .?!")

        memories = self.memory.get_all()

        # Explicitly save the current project.
        project_phrases = [
            "my current project is ",
            "my current project is called ",
            "remember that my current project is ",
            "remember my current project is ",
        ]

        for phrase in project_phrases:
            if text.startswith(phrase):
                project_name = raw_text[len(phrase):].strip().rstrip(" .!?")

                if project_name.lower().startswith("called "):
                    project_name = project_name[7:].strip()

                if project_name:
                    self.memory.remember("current_project", project_name)
                    return f"Understood. Your current project is {project_name}."

        # Retrieve the current project directly from saved memory.
        project_questions = [
            "what is my current project",
            "what's my current project",
            "tell me my current project",
            "what project am i working on",
        ]

        if any(phrase in text for phrase in project_questions):
            project = self.memory.recall("current_project")

            if project:
                return f"Your current project is {project}."

            return "I don't have your current project saved yet."

        # Explicitly save other facts.
        remember_prefixes = ["remember that ", "remember ", "save that ", "save "]

        for prefix in remember_prefixes:
            if text.startswith(prefix):
                fact = raw_text[len(prefix):].strip()

                if not fact:
                    return "What would you like me to remember?"

                normalized_fact = fact.lower()

                if "current project is" in normalized_fact:
                    value = fact.split(" is ", 1)[-1].strip().rstrip(".!?")
                    self.memory.remember("current_project", value)
                    return f"I'll remember that your current project is {value}."

                key = f"fact_{len(memories) + 1}"
                self.memory.remember(key, fact)
                return f"I'll remember that: {fact}"
                self.memory.remember(key, fact)
                return f"I'll remember that: {fact}"

        # Recall all saved memories.
        if any(phrase in text for phrase in [
            "what do you remember",
            "show my memories",
            "list my memories",
        ]):
            memories = self.memory.get_all()

            if not memories:
                return "I don't have any saved memories yet."

            return "Here is what I remember: " + "; ".join(
                f"{key}: {value}" for key, value in memories.items()
            )

        # Forget a specific memory by key.
        for prefix in ["forget ", "delete memory ", "remove memory "]:
            if text.startswith(prefix):
                key = raw_text[len(prefix):].strip().lower()

                if self.memory.forget(key):
                    return f"I've deleted the memory '{key}'."

                return f"I couldn't find a memory with the key '{key}'."

        # Normal AI conversation.
        history_text = ""

        if history:
            history_text = "\n".join(
                f"{message['role'].capitalize()}: {message['content']}"
                for message in history
            )

        memories = self.memory.get_all()
        memory_text = "\n".join(
            f"- {key}: {value}" for key, value in memories.items()
        ) or "No saved memories."

        prompt = f"""
You are JARVIS, a capable desktop AI assistant.

Saved memories:
{memory_text}

Conversation history:
{history_text}

Current user request:
{raw_text}

Use saved memories when relevant. Do not contradict explicit saved facts
without new information from the user. Respond naturally and concisely.
"""

        try:
            return self.ai.generate(prompt)
        except Exception as e:
            print("AI HANDLER ERROR:", e)
            return f"AI Error: {e}"
