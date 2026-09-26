import speech_recognition as sr
import subprocess
import time

WAKE_WORD = "jarvis"


class WakeListener:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5
        self.recognizer.dynamic_energy_threshold = True

        with sr.Microphone() as source:

            print("Calibrating wake listener...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print(
                f"Wake listener energy threshold: "
                f"{self.recognizer.energy_threshold:.2f}"
            )

    def listen(self):

        with sr.Microphone() as source:

            print("Waiting for 'Jarvis'...")

            try:

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=6
                )

            except sr.WaitTimeoutError:

                return ""

        try:

            text = self.recognizer.recognize_google(audio)

            text = text.lower().strip()

            if text:

                print(f"Heard: {text}")

            if WAKE_WORD in text:

                return text

            return ""

        except sr.UnknownValueError:

            return ""

        except sr.RequestError as e:

            print(f"Speech recognition error: {e}")

            return ""


if __name__ == "__main__":

    listener = WakeListener()

    jarvis_process = None

    while True:

        # --------------------------------
        # JARVIS IS ALREADY RUNNING
        # --------------------------------

        if jarvis_process is not None:

            if jarvis_process.poll() is None:

                time.sleep(0.5)

                continue

            # JARVIS was closed
            jarvis_process = None

            print()
            print("JARVIS closed.")
            print("Wake listener active again.")
            print()

        # --------------------------------
        # LISTEN FOR WAKE WORD
        # --------------------------------

        command = listener.listen()

        if command:

            print()
            print("=" * 50)
            print(f"WAKE DETECTED: {command}")
            print("=" * 50)
            print()

            command_after_wake_word = ""

            if command.startswith(WAKE_WORD):

                command_after_wake_word = command[
                    len(WAKE_WORD):
                ].strip()

            if command_after_wake_word:

                jarvis_process = subprocess.Popen(
                    [
                        "cmd.exe",
                        "/k",
                        r"D:\AIML projects\JARVIS AI system\venv\Scripts\python.exe",
                        r"D:\AIML projects\JARVIS AI system\main.py",
                        command_after_wake_word
                    ],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )

            else:

                jarvis_process = subprocess.Popen(
                    [
                        "cmd.exe",
                        "/k",
                        r"D:\AIML projects\JARVIS AI system\venv\Scripts\python.exe",
                        r"D:\AIML projects\JARVIS AI system\main.py",
                        "--wake"
                    ],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )