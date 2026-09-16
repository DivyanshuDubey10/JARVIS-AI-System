import os
from openai import OpenAI
from dotenv import load_dotenv
from core.tool_manager import ToolManager
import ollama

load_dotenv()


class AIService:

    def __init__(self):

        # NVIDIA cloud model
        self.nvidia_model = "nvidia/nemotron-3-super-120b-a12b"

        self.nvidia_client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Local fallback
        self.local_model = "qwen3:4b-instruct"

        self.local_client = ollama.Client(
            host="http://127.0.0.1:11434"
        )

        self.tool_manager = ToolManager()

    def generate(self, prompt):
        
        print(">>> AI GENERATE CALLED")

        try:

            response = self.nvidia_client.chat.completions.create(
                model=self.nvidia_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:

            print("NVIDIA ERROR:", repr(e))
            print("Falling back to local model...")

            try:

                response = self.local_client.chat(
                    model=self.local_model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                return response.message.content

            except Exception as local_error:

                print("OLLAMA ERROR:", repr(local_error))
                return f"AI Error: {local_error}"