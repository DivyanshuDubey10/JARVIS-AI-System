from dataclasses import dataclass


@dataclass
class Command:
    raw_text: str
    action: str = None
    target: str = None
    query: str = None
    source: str = "voice"


class CommandParser:

    # Words that can safely be removed from the beginning
    # of a command.
    POLITE_WORDS = {
        "please",
        "could",
        "would",
        "can",
        "will",
        "hey",
        "kindly"
    }

    # Words that don't provide useful information when
    # identifying a command target.
    FILLER_WORDS = {
        "my",
        "the",
        "a",
        "an",
        "for",
        "on",
        "in",
        "to"
    }

    ACTION_SYNONYMS = {

        # -----------------------------
        # OPEN
        # -----------------------------

        "open": "open",
        "launch": "open",
        "start": "open",
        "run": "open",

        # -----------------------------
        # SEARCH
        # -----------------------------

        "search": "search",
        "find": "search",
        "lookup": "search",

        # -----------------------------
        # TIME
        # -----------------------------

        "time": "time",
        "clock": "time",

        # -----------------------------
        # DATE
        # -----------------------------

        "date": "date",
        "today": "date"
    }

    KNOWN_APPS = {
        "microsoft store",
        "microsoft edge",
        "visual studio code",
        "vs code",
        "google chrome",
        "windows media player",
        "task manager",
        "control panel",

        "chrome",
        "notepad",
        "calculator",
        "paint",
        "cmd",
        "downloads",
        "documents",
        "desktop",
        "explorer",
        "whatsapp",
        "settings",
        "outlook",
        "word",
        "excel",
        "powerpoint",
        "onenote",
        "firefox",
        "spotify",
        "teams"
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

        # Remove polite words wherever they appear.
        words = [
            word
            for word in words
            if word not in self.POLITE_WORDS
        ]

        return " ".join(words)

    def find_action(self, words):

        # Multi-word actions first
        for i in range(len(words) - 1):

            phrase = f"{words[i]} {words[i + 1]}"

            if phrase == "look up":
                return "search"

        # Single-word actions
        for word in words:

            if word in self.ACTION_SYNONYMS:
                return self.ACTION_SYNONYMS[word]

        return None

    def find_target(self, words):

        # Check multi-word targets first.
        for app in sorted(
            self.KNOWN_APPS,
            key=lambda x: len(x.split()),
            reverse=True
        ):

            app_words = app.split()

            for i in range(
                len(words) - len(app_words) + 1
            ):

                if words[i:i + len(app_words)] == app_words:
                    return app

        # Then check websites.
        for website in self.KNOWN_WEBSITES:

            if website in words:
                return website

        return None

    def parse_search(self, words, action_index):

        # Everything after the search action.
        remaining = words[action_index + 1:]

        if not remaining:
            return None, None

        target = None

        # Look for a known search engine / website.
        for word in remaining:

            if word in self.KNOWN_WEBSITES:
                target = word
                break

        if target:

            # Remove the target and common filler words.
            query_words = []

            for word in remaining:

                if word == target:
                    continue

                if word in self.FILLER_WORDS:
                    continue

                query_words.append(word)

            query = " ".join(query_words)

            return target, query

        # No known engine specified.
        # Use Google as default.
        query_words = [
            word
            for word in remaining
            if word not in self.FILLER_WORDS
        ]

        query = " ".join(query_words)

        return "google", query

    def parse_open(self, words, action_index):

        remaining = words[action_index + 1:]

        if not remaining:
            return None

        # Prefer a known target anywhere after "open".
        target = self.find_target(remaining)

        if target:
            return target

        # Otherwise use the first meaningful word.
        for word in remaining:

            if word not in self.FILLER_WORDS:
                return word

        return None

    def parse(self, text):

        # Preserve exactly what the user said for AI.
        original_text = text.lower().strip()

        if not original_text:
            return None

        command_text = self.clean_text(
            original_text
        )

        words = command_text.split()

        if not words:
            return None

        action = self.find_action(words)

        target = None
        query = None

        # --------------------------------
        # NO ACTION
        # --------------------------------

        if action is None:

            return Command(
                raw_text=original_text,
                action=None,
                target=None,
                query=None
            )

        # --------------------------------
        # FIND ACTION POSITION
        # --------------------------------

        action_index = None

        # Multi-word action: "look up"
        for index in range(len(words) - 1):

            phrase = f"{words[index]} {words[index + 1]}"

            if phrase == "look up":

                action_index = index
                break

        # Single-word action
        if action_index is None:

            for index, word in enumerate(words):

                if word in self.ACTION_SYNONYMS:

                    action_index = index
                    break

        if action_index is None:

            return Command(
                raw_text=original_text,
                action=action
            )

        # --------------------------------
        # OPEN
        # --------------------------------

        if action == "open":

            target = self.parse_open(
                words,
                action_index
            )

        # --------------------------------
        # SEARCH
        # --------------------------------

        elif action == "search":

            target, query = self.parse_search(
                words,
                action_index
            )

        # --------------------------------
        # TIME / DATE
        # --------------------------------

        elif action in ["time", "date"]:

            pass

        return Command(
            raw_text=original_text,
            action=action,
            target=target,
            query=query
        )