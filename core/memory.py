class ConversationMemory:
    def __init__(self, max_messages = 10):
        self.max_messages = max_messages
        self.messages = []
        
    def add_user(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })
        self.trim()
        
    def add_assistant(self, message):
        self.messages.append({
            "role": "assistant",
            "content": message
        })
        self.trim()
        
    def trim(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
            
    def get_messages(self):
        return self.messages
    
    def clear(self):
        self.messages.clear()