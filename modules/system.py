import os
import subprocess
import re

from datetime import datetime


class SystemHandler:

    def __init__(self):

        self.apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "cmd": "cmd.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "explorer": "explorer.exe"
        }

        self.folders = {
            "downloads": os.path.join(
                os.path.expanduser("~"),
                "Downloads"
            ),

            "documents": os.path.join(
                os.path.expanduser("~"),
                "Documents"
            ),

            "desktop": os.path.join(
                os.path.expanduser("~"),
                "Desktop"
            )
        }

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

            return datetime.now().strftime(
                "%I:%M %p"
            )

        # -----------------------------
        # DATE
        # -----------------------------

        elif command.action == "date":

            return datetime.now().strftime(
                "%d %B %Y"
            )

        # -----------------------------
        # OPEN
        # -----------------------------

        elif command.action == "open":

            target = command.target

            # Open application
            if target in self.apps:

                subprocess.Popen(
                    self.apps[target]
                )

                return f"Opening {target.title()}..."

            # Open folder
            if target in self.folders:

                os.startfile(
                    self.folders[target]
                )

                return f"Opening {target.title()}..."

        return None