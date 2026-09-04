import ollama


class AIService:

    def __init__(self):

        self.model = "qwen3:4b"

        self.client = ollama.Client(
            host="http://127.0.0.1:11434"
        )

    def generate(self, prompt):

        try:

            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\n/no_think"
                    }
                ],
                options={
                    "temperature": 0.4,
                    "num_predict": 150
                },
                think=False
            )
            
            return response.message.content
            
            
        except Exception as e:

            print("OLLAMA ERROR:", repr(e))

            return f"AI Error: {e}"