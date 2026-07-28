from datetime import datetime

class Router:
    def handle(self, command):
        command = command.lower()
        
        if "time" in command:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}"
        
        elif "date" in command:
            return f"Tpday's date is {datetime.now().strftime('%d %B %Y')}"
        
        else:
            return "Sorry, I don't understand that command yet."