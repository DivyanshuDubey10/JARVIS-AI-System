from core.router import CommandRouter
from core.parser import CommandParser

class Assistant:
    def __init__(self): 
        self.router = CommandRouter()
        self.parser = CommandParser()

    def run(self):
        print("=" * 50)
        print("JARVIS AI SYSTEM")
        print("Type 'exit' to quit.")
        print("=" * 50)
        
        while True:
            command = input("\nYou: ").strip()
            
            if not command:
                continue 
            if command.lower() == "exit":
                print("Jarvis: Goodybye!")
                break
            
            parsed_command = self.parser.parse(command)
            response = self.router.handle(parsed_command)
            
            print(f"Jarvis: {response}")