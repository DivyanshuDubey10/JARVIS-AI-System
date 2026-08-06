from core.router import CommandRouter
from core.parser import CommandParser
from core.speech import SpeechEngine
from voice.listener import VoiceListener
from core.memory import ConversationMemory

class Assistant:
    def __init__(self):
        self.router = CommandRouter()
        self.parser = CommandParser()
        self.memory = ConversationMemory()
        self.listener = VoiceListener() 
        self.speech = SpeechEngine()

    def run(self):
        print("=" * 50)
        print("JARVIS AI SYSTEM")
        print("Type 'exit' to quit.")
        print("=" * 50)

        while True:
            command = self.listener.listen()

            if not command:
                continue

            if command.lower() == "exit":
                self.respond("Goodbye!")
                break

            parsed_command = self.parser.parse(command)
            response = self.router.handle(parsed_command, self.memory.get_messages())

            self.memory.add_assistant(response)
            self.respond(response)

    def respond(self, message):
        print(f"Jarvis: {message}")
        self.speech.speak(message)