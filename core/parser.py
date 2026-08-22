from dataclasses import dataclass


@dataclass
class Command:
    raw_text: str
    action: str = None
    target: str = None
    query: str = None
    source: str = "voice"


class CommandParser:

    # Only remove words that are safe to remove from command prefixes.
    # DO NOT remove normal conversational words like "you".
    POLITE_WORDS = {
        "please",
        "could",
        "would",
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
        "cmd",
        "downloads",
        "documents",
        "desktop",
        "explorer",
        "whatsapp"
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
        words = text.lower().strip().split()

        # Remove only polite/filler words.
        # Keep words like "you", "the", "a", etc.
        while words and words[0] in self.POLITE_WORDS:
            words.pop(0)

        return " ".join(words)

    def parse(self, text):

        # Preserve the user's actual words for AI.
        original_text = text.lower().strip()

        if not original_text:
            return None

        # Remove only optional command prefixes for command detection.
        command_text = self.clean_text(original_text)

        words = command_text.split()

        if not words:
            return None

        action = None
        target = None
        query = None

        # Find an action.
        for word in words:
            if word in self.ACTION_SYNONYMS:
                action = self.ACTION_SYNONYMS[word]
                break

        # Find known application or website.
        for word in words:
            if word in self.KNOWN_APPS:
                target = word
                break

            if word in self.KNOWN_WEBSITES:
                target = word
                break

        # Handle structured commands.
        if action is not None:

            action_index = None

            for i, word in enumerate(words):
                if word in self.ACTION_SYNONYMS:
                    action_index = i
                    break

            if action_index is not None:

                remaining = words[action_index + 1:]

                if remaining:
                    if target is None:
                        target = remaining[0]

                    if len(remaining) > 1:
                        query = " ".join(remaining[1:])

        # IMPORTANT:
        # raw_text contains the user's actual question,
        # not the command-cleaned version.
        return Command(
            raw_text=original_text,
            action=action,
            target=target,
            query=query
        )