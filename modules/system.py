import os
import subprocess
import re

from datetime import datetime


class SystemHandler:

    def __init__(self):

        self.apps = {

            # =============================
            # WINDOWS
            # =============================

            "settings": "ms-settings:",
            "microsoft store": "ms-windows-store:",
            "explorer": r"shell:AppsFolder\Microsoft.Windows.Explorer",
            "file explorer": r"shell:AppsFolder\Microsoft.Windows.Explorer",

            "calculator": r"shell:AppsFolder\Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",

            "camera": r"shell:AppsFolder\Microsoft.WindowsCamera_8wekyb3d8bbwe!App",

            "clock": r"shell:AppsFolder\Microsoft.WindowsAlarms_8wekyb3d8bbwe!App",

            "game bar": r"shell:AppsFolder\Microsoft.XboxGamingOverlay_8wekyb3d8bbwe!App",

            "get help": r"shell:AppsFolder\Microsoft.GetHelp_8wekyb3d8bbwe!App",

            # =============================
            # BASIC WINDOWS PROGRAMS
            # =============================

            "notepad": "notepad.exe",
            "paint": "mspaint.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "powershell": "powershell.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",

            # =============================
            # BROWSERS
            # =============================

            "chrome": r"shell:AppsFolder\Chrome",
            "google chrome": r"shell:AppsFolder\Chrome",

            "edge": r"shell:AppsFolder\MSEdge",
            "microsoft edge": r"shell:AppsFolder\MSEdge",

            "brave": r"shell:AppsFolder\Brave",

            # =============================
            # DEVELOPMENT
            # =============================

            "visual studio code":
                r"shell:AppsFolder\Microsoft.VisualStudioCode",

            "vs code":
                r"shell:AppsFolder\Microsoft.VisualStudioCode",

            "vscode":
                r"shell:AppsFolder\Microsoft.VisualStudioCode",

            "cursor":
                r"shell:AppsFolder\Anysphere.Cursor",

            "antigravity":
                r"shell:AppsFolder\Google.Antigravity",

            "antigravity ide":
                r"shell:AppsFolder\Google.AntigravityIDE",

            # =============================
            # COMMUNICATION
            # =============================

            "whatsapp":
                r"shell:AppsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",

            "teams":
                r"shell:AppsFolder\MSTeams_8wekyb3d8bbwe!MSTeams",

            # =============================
            # MICROSOFT
            # =============================

            "outlook":
                r"shell:AppsFolder\Microsoft.OutlookForWindows_8wekyb3d8bbwe!Microsoft.OutlookforWindows",

            "onenote":
                r"shell:AppsFolder\Microsoft.Office.OneNote_8wekyb3d8bbwe!microsoft.onenoteim",

            # =============================
            # MICROSOFT OFFICE 2010
            # =============================

            "word":
                r"shell:AppsFolder\{7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\Microsoft Office\Office14\WINWORD.EXE",

            "excel":
                r"shell:AppsFolder\{7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\Microsoft Office\Office14\EXCEL.EXE",

            "powerpoint":
                r"shell:AppsFolder\{7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\Microsoft Office\Office14\POWERPNT.EXE",
        }

        self.folders = {
            "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
            "videos": os.path.join(os.path.expanduser("~"), "Videos"),
            "music": os.path.join(os.path.expanduser("~"), "Music"),
            "favorites": os.path.join(os.path.expanduser("~"), "Favorites"),
            "contacts": os.path.join(os.path.expanduser("~"), "Contacts"),
            "links": os.path.join(os.path.expanduser("~"), "Links"),
            "saved games": os.path.join(os.path.expanduser("~"), "Saved Games"),
        }
        
    def open_app(self, app_name):
        if app_name in self.apps:
            subprocess.Popen(self.apps[app_name])
            return f"Opening {app_name.title()}..."
        return f"Application '{app_name}' not found."

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

                if target in self.apps:

                    app_path = self.apps[target]

                    if app_path.startswith("shell:"):

                        subprocess.Popen(
                            ["explorer.exe", app_path]
                        )

                    elif app_path.endswith(":"):

                        subprocess.Popen(
                            [
                                "powershell",
                                "-Command",
                                f'Start-Process "{app_path}"'
                            ]
                        )

                    else:

                        subprocess.Popen(app_path)

                    return f"Opening {target.title()}..."

            # Open folder
            if target in self.folders:

                os.startfile(
                    self.folders[target]
                )

                return f"Opening {target.title()}..."

        return None