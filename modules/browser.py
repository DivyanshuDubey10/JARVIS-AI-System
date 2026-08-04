import webbrowser

class BrowserHandler:
    def __init__(self):
        self.websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://www.github.com",
            #Shopping
            "amazon": "https://www.amazon.com",
            #AI
            "chatgpt": "https://chatgpt.com",
            "gemini": "https://www.gemini.com",
            "claude": "https://www.claude.ai",
            #Dimag
            "wikipedia": "https://www.wikipedia.org",
            #Social
            "linkedin": "https://www.linkedin.com",
            "instagram": "https://instagram.com",
            #Streaming
            "spotify": "https://open.spotify.com",
            "netflix": "https://netflix.com",
            "prime": "https://www.primevideo.com",
            "gmail": "https://mail.google.com"
        }
        self.search_engines = {
            "google": "https://www.google.com/search?q={query}",
            "youtube": "https://www.youtube.com/results?search_query={query}",
            "github": "https://github.com/search?q={query}"
        }
    def handle(self, command):   
        command = command.lower()
        
        if command.startswith("open "):
            website = command.replace("open ", "").strip()
            
            if website in self.websites:
                webbrowser.open(self.websites[website])
                return f"Opening {website.title()}..."
            
            if "." in website:
                webbrowser.open(f"https://{website}")
                return f"Opening {website}..."
            
            webbrowser.open(f"https://www.{website}.com")
            return f"trying to open {website.title()}..."
        
        return None