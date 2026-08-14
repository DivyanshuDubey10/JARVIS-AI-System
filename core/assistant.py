import time 
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
        self.awake = False
        self.last_activity = time.time()

    def run(self):

        print("=" * 50)
        print("JARVIS AI SYSTEM")
        print("Type 'exit' to quit.")
        print("=" * 50)

        WAKE_WORD = "jarvis"

        while True:
            if self.awake and time.time() - self.last_activity > 30:
                print("Going back to sleep...")
                self.awake = False

            command = self.listener.listen()

            if not command:
                continue

            # Exit
            if command == "exit":
                self.respond("Goodbye.")
                break

            # Stop
            if command in ["stop", "cancel", "quiet"]:
                self.speech.stop()
                continue

            # --------------------------------
            # WAKE WORD / COMMAND HANDLING
            # --------------------------------

            if command == WAKE_WORD:
                self.awake = True
                self.last_activity = time.time()
                self.respond("Yes?")
                continue

            # "jarvis open chrome"
            if command.startswith(WAKE_WORD + " "):
                self.awake = True
                self.last_activity = time.time()
                command = command[len(WAKE_WORD):].strip()

            # Normal command without wake word
            else:
                self.last_activity = time.time()

            # --------------------------------
            # ACTIVE CONVERSATION
            # --------------------------------

            self.last_activity = time.time()
            
            if command.lower() in [
                "what did i ask",
                "what did i ask you",
                "what was my question",
                "what did i just ask",
                "what did i just ask you"
            ]:
                
                user_messages = [
                message["content"]
                for message in self.memory.get_messages()
                if message["role"] == "user"
                ]

                if user_messages:
                    self.respond(f"You asked: {user_messages[-1]}")
                else:
                    self.respond("You haven't asked me anything yet.")

                continue

            parsed_command = self.parser.parse(command)

            if parsed_command is None:
                continue

            history = self.memory.get_messages()

            response = self.router.handle(
                parsed_command,
                history
            )

            self.memory.add_user(parsed_command.raw_text)

            if response:
                self.memory.add_assistant(response)
                self.respond(response)
            
    def respond(self, message):
        if not message:
            return 
        
        print(f"Jarvis: {message}")
        self.speech.speak(message)