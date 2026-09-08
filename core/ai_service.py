import ollama


class AIService:

    def __init__(self):

        self.model = "qwen3:4b-instruct"

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
                    "num_predict": 500
                },
                think=False
            )
            
            content = response.message.content
            if "</think>" in content:
                content = content.split("</think>")[-1].strip()
            return content
        
            
            
        except Exception as e:

            print("OLLAMA ERROR:", repr(e))

            return f"AI Error: {e}"