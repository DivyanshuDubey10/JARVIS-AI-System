import time
from core.router import CommandRouter
from core.parser import CommandParser
from core.speech import SpeechEngine
from voice.listener import VoiceListener
from core.memory import ConversationMemory


class Assistant:

    def __init__(self):

        self.parser = CommandParser()
        self.memory = ConversationMemory()
        self.listener = VoiceListener()
        self.speech = SpeechEngine()

        # Messages from background tasks are placed here.
        self.pending_messages = []

        self.router = CommandRouter(
            timer_callback=self.queue_message
        )

        self.awake = False
        self.last_activity = time.time()

    def queue_message(self, message):
        """Receive messages from background tasks."""
        if message:
            self.pending_messages.append(message)
            
    def run_countdown(self, seconds):

        # Short timers get a spoken countdown.
        if seconds <= 30:

            end_time = time.monotonic() + seconds

            for number in range(seconds, 0, -1):

                # Wait until the correct countdown point.
                target_time = end_time - (number - 1)

                remaining_wait = target_time - time.monotonic()

                if remaining_wait > 0:
                    time.sleep(remaining_wait)

                # Speak the number.
                self.respond(str(number))

            self.respond("Time's up.")

        else:

            # Long timers don't speak every number.
            time.sleep(seconds)

            self.respond("Time's up.")
            
            
    def run_countdown(self, seconds):

        if seconds <= 30:

            end_time = time.monotonic() + seconds

            for number in range(seconds, 0, -1):

                target_time = end_time - (number - 1)

                remaining_wait = target_time - time.monotonic()

                if remaining_wait > 0:
                    time.sleep(remaining_wait)

                self.respond(str(number))

            self.respond("Time's up.")

        else:

            time.sleep(seconds)

            self.respond("Time's up.")
            
            
    def run(self):

        print("=" * 50)
        print("JARVIS AI SYSTEM")
        print("Type 'exit' to quit.")
        print("=" * 50)

        WAKE_WORD = "jarvis"

        while True:

            # --------------------------------
            # BACKGROUND MESSAGES
            # --------------------------------

            if self.pending_messages:

                message = self.pending_messages.pop(0)
                self.respond(message)
                continue

            # --------------------------------
            # SLEEP TIMEOUT
            # --------------------------------

            if self.awake and time.time() - self.last_activity > 30:
                print("Going back to sleep...")
                self.awake = False

            # --------------------------------
            # LISTEN
            # --------------------------------

            command = self.listener.listen()

            if not command:
                continue

            # --------------------------------
            # EXIT
            # --------------------------------

            if command == "exit":
                self.respond("Goodbye.")
                break

            # --------------------------------
            # STOP
            # --------------------------------

            if command in ["stop", "cancel", "quiet"]:
                self.speech.stop()
                continue

            # --------------------------------
            # WAKE WORD
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

            else:
                self.last_activity = time.time()

            # --------------------------------
            # MEMORY QUESTION
            # --------------------------------

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
                    self.respond(
                        f"You asked: {user_messages[-1]}"
                    )
                else:
                    self.respond(
                        "You haven't asked me anything yet."
                    )

                continue

            # --------------------------------
            # PARSE COMMAND
            # --------------------------------

            parsed_command = self.parser.parse(command)

            if parsed_command is None:
                continue

            # --------------------------------
            # AI / SYSTEM / BROWSER
            # --------------------------------

            history = self.memory.get_messages()

            response = self.router.handle(
                parsed_command,
                history
            )

            # Store user's message ONCE
            self.memory.add_user(
                parsed_command.raw_text
            )

            # --------------------------------
            # TIMER
            # --------------------------------

            if isinstance(response, dict) and response.get("type") == "timer":

                message = response["message"]
                seconds = response["seconds"]

                self.memory.add_assistant(message)

                # Speak confirmation first
                self.respond(message)

                # Run countdown
                self.run_countdown(seconds)

                continue

            # --------------------------------
            # NORMAL RESPONSE
            # --------------------------------

            if response:

                self.memory.add_assistant(response)

                self.respond(response)

    def respond(self, message):

        if not message:
            return

        print(f"Jarvis: {message}")

        self.speech.speak(message)