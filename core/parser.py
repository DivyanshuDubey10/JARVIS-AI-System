from dataclasses import dataclass


@dataclass
class Command:
    raw_text: str
    action: str = None
    target: str = None
    query: str = None
    source: str = "voice"


class CommandParser:

    STOP_WORDS = {
        "please",
        "can",
        "could",
        "would",
        "you",
        "the",
        "a",
        "an",
        "jarvis",
        "hey"
    }
    
    ACTION_SYNONYMS = {
    # Open
    "open": "open",
    "launch": "open",
    "start": "open",
    "run": "open",

    # Search
    "search": "search",
    "find": "search",
    "lookup": "search",

    # Time
    "time": "time",
    "clock": "time",

    # Date
    "date": "date",
    "today": "date"
    }
    KNOWN_APPS = {
    "chrome",
    "notepad",
    "calculator",
    "paint",
    "cmd"
    }

    KNOWN_WEBSITES = {
        "youtube",
        "github",
        "google",
        "gmail",
        "linkedin",
        "spotify",
        "instagram",
        "amazon",
        "chatgpt",
        "claude",
        "gemini",
        "netflix",
        "prime",
        "wikipedia"
    }

    def clean_text(self, text):
        words = text.lower().split()

        words = [
            word for word in words
            if word not in self.STOP_WORDS
        ]

        return " ".join(words)

    def parse(self, text):

        text = self.clean_text(text)

        words = text.split()

        if not words:
            return None
        
        target = None

        for word in words:
            if word in self.KNOWN_APPS:
                target = word
                break

            if word in self.KNOWN_WEBSITES:
                target = word
                break

        for word in words:
            if word in self.ACTION_SYNONYMS:
                action = self.ACTION_SYNONYMS[word]
                break
        else:
            action = None

        target = words[1] if len(words) > 1 else None
        query = " ".join(words[2:]) if len(words) > 2 else None

        return Command(text, action, target, query)