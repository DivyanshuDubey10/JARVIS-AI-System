import webbrowser
from urllib.parse import quote_plus


class BrowserHandler:

    def __init__(self):

        self.websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://www.github.com",

            # Shopping
            "amazon": "https://www.amazon.com",

            # AI
            "chatgpt": "https://chatgpt.com",
            "gemini": "https://gemini.google.com",
            "claude": "https://claude.ai",

            # Information
            "wikipedia": "https://www.wikipedia.org",

            # Social
            "linkedin": "https://www.linkedin.com",
            "instagram": "https://instagram.com",

            # Streaming
            "spotify": "https://open.spotify.com",
            "netflix": "https://netflix.com",
            "prime": "https://www.primevideo.com",

            # Email
            "gmail": "https://mail.google.com"
        }

        self.search_engines = {
            "google": "https://www.google.com/search?q={query}",
            "youtube": "https://www.youtube.com/results?search_query={query}",
            "github": "https://github.com/search?q={query}",
            "wikipedia": "https://en.wikipedia.org/wiki/Special:Search?search={query}"
        }

    def handle(self, command):

        # -----------------------------
        # OPEN WEBSITE
        # -----------------------------

        if command.action == "open":

            website = command.target

            if website is None:
                return "What would you like me to open?"

            if website in self.websites:

                webbrowser.open(
                    self.websites[website]
                )

                return f"Opening {website.title()}..."

            if "." in website:

                webbrowser.open(
                    f"https://{website}"
                )

                return f"Opening {website}..."

            webbrowser.open(
                f"https://www.{website}.com"
            )

            return f"Trying to open {website.title()}..."

        # -----------------------------
        # SEARCH
        # -----------------------------

        if command.action == "search":

            engine = command.target
            query = command.query

            if not query:
                return "What would you like me to search for?"

            if engine not in self.search_engines:

                engine = "google"

                # If the parser interpreted the first word
                # as the search target, include it in the query.
                if command.target:
                    query = f"{command.target} {query}"

            encoded_query = quote_plus(query)

            url = self.search_engines[engine].format(
                query=encoded_query
            )

            webbrowser.open(url)

            return f"Searching {engine.title()} for {query}..."

        return None