from modules.system import SystemHandler
from modules.browser import BrowserHandler

class CommandRouter:
    def __init__(self):
        self.handlers = [
            SystemHandler(),
            BrowserHandler(),
        ]
    def handle(self, command):
        for handler in self.handlers:
            result = handler.handle(command)
            if result is not None:
                return result
             
        return "Sorry, I don't understand."