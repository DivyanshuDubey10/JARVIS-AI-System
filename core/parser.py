class Command:
    def __init__(self, raw, action, target=None, query=""):
        self.raw = raw
        self.action = action
        self.target = target
        self.query = query

class CommandParser:
    def parse(self, text):
        text = text.lower().strip()
        
        words= text.split()
        
        if not words:
            return None
        
        action = words[0]
        target = words[1] if len(words) > 1 else None
        query = " ".join(words[2:]) if len(words) > 2 else " "

        return Command(text, action, target, query)

