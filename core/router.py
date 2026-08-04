from modules.system import SystemHandler

class Router:
    def __init__(self):
        self.system = SystemHandler()
    
    def handle(self, command):
        result = self.system.handle(command)
        
        if result:
            return result 
        return "Sorry, I don't understand."