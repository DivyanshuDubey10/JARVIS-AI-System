import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET


class NewsHandler:

    def handle(self, command):

        text = command.raw_text.lower()

        if not self.is_news_request(text):
            return None

        return self.get_news()

    def is_news_request(self, text):

        keywords = [
            "news",
            "headlines",
            "latest news",
            "today's news",
            "today news",
            "what's happening",
            "what is happening"
        ]

        return any(keyword in text for keyword in keywords)

    def get_news(self):

        url = (
            "https://news.google.com/rss/search?"
            + urllib.parse.urlencode({
                "q": "news when:1d",
                "hl": "en-IN",
                "gl": "IN",
                "ceid": "IN:en"
            })
        )

        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "JARVIS-AI-System/1.0"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=10
            ) as response:

                data = response.read()

            root = ET.fromstring(data)

            articles = root.findall(".//item")

            if not articles:
                return "I couldn't find any news right now."

            headlines = []

            for article in articles[:5]:

                title = article.findtext("title")

                if title:
                    headlines.append(title)

            if not headlines:
                return "I couldn't find any news right now."

            response_text = "Here are the latest headlines. "

            for index, headline in enumerate(headlines, start=1):
                response_text += f"{index}. {headline}. "

            return response_text

        except Exception as e:

            print("NEWS ERROR:", e)

            return "Sorry, I couldn't retrieve the latest news right now."