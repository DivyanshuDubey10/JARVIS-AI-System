import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()


class AIService:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.models = [
            "gemini-3.6-flash",
            "gemini-3.5-flash",
            "gemini-flash-latest"
        ]

    def generate(self, prompt):

        last_error = None

        for model in self.models:

            for attempt in range(3):

                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt
                    )
                    return response.text

                except Exception as e:
                    last_error = e

                    if "503" in str(e):
                        print(f"{model} is busy... retrying.")
                        time.sleep(2)
                        continue

                    break

        return f"AI Error: {last_error}"