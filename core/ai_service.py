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

        try:

            tool_definitions = self.tool_manager.get_tool_definitions()

            response = self.nvidia_client.chat.completions.create(
                model=self.nvidia_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                tools=[
                    {
                        "type": "function",
                        "function": tool
                    }
                    for tool in tool_definitions
                ],
                max_tokens=500,
                temperature=0.7
            )

            message = response.choices[0].message

            # --------------------------------
            # TOOL CALL
            # --------------------------------

            if message.tool_calls:

                tool_call = message.tool_calls[0]

                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments

                import json

                arguments = json.loads(arguments)

                print()
                print("AI TOOL CALL:")
                print(f"Tool: {tool_name}")
                print(f"Arguments: {arguments}")
                print()

                result = self.tool_manager.execute(
                    tool_name,
                    **arguments
                )

                print("TOOL RESULT:")
                print(result)

                # --------------------------------
                # SEND TOOL RESULT BACK TO AI
                # --------------------------------

                follow_up = self.nvidia_client.chat.completions.create(
                    model=self.nvidia_model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        },
                        {
                            "role": "assistant",
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": tool_name,
                                        "arguments": tool_call.function.arguments
                                    }
                                }
                            ]
                        },
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result)
                        }
                    ],
                    max_tokens=500,
                    temperature=0.7
                )

                return follow_up.choices[0].message.content

            # --------------------------------
            # NORMAL AI RESPONSE
            # --------------------------------

            return message.content

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