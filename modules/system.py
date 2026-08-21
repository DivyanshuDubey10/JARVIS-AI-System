import subprocess
import threading
import time
import re
from datetime import datetime


class SystemHandler:

    def __init__(self, timer_callback=None):

        self.timer_callback = timer_callback

        self.apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "cmd": "cmd.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        }

    def start_timer(self, seconds):
        return seconds

    def handle(self, command):

        query = command.raw_text.lower()

        # -----------------------------
        # TIMER
        # -----------------------------

        if "timer" in query:

            match = re.search(
                r'(\d+)\s*(second|seconds|minute|minutes|hour|hours)',
                query
            )

            if match:

                amount = int(match.group(1))
                unit = match.group(2)

                if "second" in unit:
                    seconds = amount

                elif "minute" in unit:
                    seconds = amount * 60

                else:
                    seconds = amount * 3600

                return {
                    "type": "timer",
                    "seconds": seconds,
                    "message": f"Timer set for {amount} {unit}."
                }

            return "Please specify how long you want the timer to be."

        # -----------------------------
        # TIME
        # -----------------------------

        if command.action == "time":

            return datetime.now().strftime("%I:%M %p")

        # -----------------------------
        # DATE
        # -----------------------------

        elif command.action == "date":

            return datetime.now().strftime("%d %B %Y")

        # -----------------------------
        # OPEN APP
        # -----------------------------

        elif command.action == "open":

            app = command.target

            if app in self.apps:

                subprocess.Popen(
                    self.apps[app]
                )

                return f"Opening {app.title()}..."

        return None