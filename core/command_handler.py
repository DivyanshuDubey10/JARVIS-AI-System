from datetime import datetime 

class CommandHandler:
    def handle(self, command: str):
        command = command.lower()
        if "time" in command:
            return datetime.now().strftime("%I:%M:%p")
        
        elif "date" in command:
            return datetime.now().strftime("%d %B %Y")
        
        else:
            return "Sorry, I don't understan that command yet."
        