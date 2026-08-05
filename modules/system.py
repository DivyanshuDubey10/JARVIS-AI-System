import subprocess
from datetime import datetime

from core.parser import Command

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
        
        if command.action == "time":
            return datetime.now().strftime("%I:%M %p")
        
        elif command.action == "date":
            return datetime.now().strftime("%d %B %Y")
        elif command.action == "open":
            app = command.target
            
            if app in self.apps:
                subprocess.Popen(self.apps[app])
                return f"Opening {app.title()}..."
        return None