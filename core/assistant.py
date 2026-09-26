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

        self.router = CommandRouter()

        self.awake = False
        self.last_activity = time.time()

    # --------------------------------
    # TIMER
    # --------------------------------

    def run_countdown(self, seconds):

        if seconds <= 30:

            end_time = time.monotonic() + seconds

            for number in range(seconds, 0, -1):

                target_time = end_time - (number - 1)

                remaining_wait = (
                    target_time - time.monotonic()
                )

                if remaining_wait > 0:
                    time.sleep(remaining_wait)

                self.respond(str(number))

            self.respond("Time's up.")

        else:

            time.sleep(seconds)

            self.respond("Time's up.")

    # --------------------------------
    # MAIN LOOP
    # --------------------------------

    def run(self, initial_command=None):

        print("=" * 60)
        print("                 JARVIS AI SYSTEM")
        print("=" * 60)
        print()
        print("Status   : ONLINE")
        print("Voice    : ACTIVE")
        print("AI       : NVIDIA Nemotron")
        print("Fallback : Qwen3 4B Instruct")
        print()
        print("-" * 60)
        print('Say "Jarvis" to wake me.')
        print("-" * 60)
        print()

        WAKE_WORD = "jarvis"
        
        if initial_command is not None:

            self.awake = True
            self.last_activity = time.time()

            command = initial_command.strip()

            if command:
                parsed_command = self.parser.parse(command)

                if parsed_command is not None:

                    history = self.memory.get_messages()

                    response = self.router.handle(
                        parsed_command,
                        history
                    )

                    self.memory.add_user(
                        parsed_command.raw_text
                    )

                    if (
                        isinstance(response, dict)
                        and response.get("type") == "timer"
                    ):

                        message = response["message"]
                        seconds = response["seconds"]

                        self.memory.add_assistant(
                            message
                        )

                        self.respond(message)

                        self.run_countdown(seconds)

                    elif response:

                        self.memory.add_assistant(
                            response
                        )

                        self.respond(response)

        while True:

            # --------------------------------
            # SLEEP MODE
            # --------------------------------

            if not self.awake:

                command = self.listener.listen_for_wake_word()

                if not command:
                    continue

                if command == WAKE_WORD:

                    self.awake = True
                    self.last_activity = time.time()

                    self.respond("Yes Sir?")

                continue

            # --------------------------------
            # ACTIVE MODE
            # --------------------------------

            command = self.listener.listen_for_command()

            if not command:
                continue

            # --------------------------------
            # EXIT
            # --------------------------------

            if command.lower() in [
                "exit",
                "goodbye",
                "quit",
                "bye"
            ]:

                self.respond("Goodbye.")

                break

            # --------------------------------
            # STOP
            # --------------------------------

            if command.lower() in [
                "stop",
                "cancel",
                "quiet"
            ]:

                self.speech.stop()

                continue

            # --------------------------------
            # WAKE WORD + COMMAND
            # --------------------------------

            if command.startswith(WAKE_WORD + " "):

                command = command[
                    len(WAKE_WORD):
                ].strip()

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

                    for message
                    in self.memory.get_messages()

                    if message["role"] == "user"

                ]

                if user_messages:

                    self.respond(
                        f"You asked: "
                        f"{user_messages[-1]}"
                    )

                else:

                    self.respond(
                        "You haven't asked me anything yet."
                    )

                continue

            # --------------------------------
            # PARSE COMMAND
            # --------------------------------

            parsed_command = self.parser.parse(
                command
            )

            if parsed_command is None:
                continue

            # --------------------------------
            # ROUTER
            # --------------------------------

            history = self.memory.get_messages()

            response = self.router.handle(
                parsed_command,
                history
            )

            # --------------------------------
            # MEMORY
            # --------------------------------

            self.memory.add_user(
                parsed_command.raw_text
            )

            # --------------------------------
            # TIMER
            # --------------------------------

            if (
                isinstance(response, dict)
                and response.get("type") == "timer"
            ):

                message = response["message"]
                seconds = response["seconds"]

                self.memory.add_assistant(
                    message
                )

                self.respond(message)

                self.run_countdown(
                    seconds
                )

                continue

            # --------------------------------
            # NORMAL RESPONSE
            # --------------------------------

            if response:

                self.memory.add_assistant(
                    response
                )

                self.respond(response)

    # --------------------------------
    # SPEAK
    # --------------------------------

    def respond(self, message):

        if not message:
            return

        print(
            f"Jarvis: {message}"
        )

        self.speech.speak(
            message
        )