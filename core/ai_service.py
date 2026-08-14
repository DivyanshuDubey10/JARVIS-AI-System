import ollama


class AIService:

    def __init__(self):
        self.model = "qwen3:1.7b"

    def generate(self, prompt):

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.4,
                    "num_predict": 150
                },
                think = False
            )

            return response.message.content

        except Exception as e:
            print("OLLAMA ERROR:", e)
            return f"AI Error: {e}"