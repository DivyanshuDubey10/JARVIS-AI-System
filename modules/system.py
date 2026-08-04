import subprocess
from datetime import datetime

class SystemHandler:
    def __init__(self):
        self.apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "cmd": "cmd.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        }
        
    def handle(self, command):
        command = command.lower()
        
        if "time" in command:
            return datetime.now().strftime("%I:%M %p")
        
        elif "date" in command:
            return datetime.now().strftime("%d %B %Y")
        elif command.startswith("open "):
            app = command.replace("open ", "").strip()
            
            if app in self.apps:
                subprocess.Popen(self.apps[app])
                return f"Opening {app.title()}..."
        return None