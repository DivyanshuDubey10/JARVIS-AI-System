from core.router import Router

class Assistant:
    def __init__(self):
        self.router = Router()
        
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
            
            response = self.router.handle(command)
            
            print(f"Jarvis: {response}")