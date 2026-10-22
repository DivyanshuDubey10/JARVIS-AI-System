import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from core.tool_manager import ToolManager

load_dotenv()


class AIService:

    def __init__(self):

        self.nvidia_model = "nvidia/nemotron-3-ultra-550b-a55b"

        self.nvidia_client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=(
                os.getenv("OPENAI_API_KEY")
            ),
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
                        "content": prompt,
                    }
                ],
                tools=[
                    {
                        "type": "function",
                        "function": tool,
                    }
                    for tool in tool_definitions
                ],
                max_tokens=500,
                temperature=0.7,
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return message.content or "NVIDIA returned an empty response."

            # Execute the first requested tool.
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"\nAI TOOL CALL: {tool_name}")
            print(f"Arguments: {arguments}")

            result = self.tool_manager.execute(
                tool_name,
                **arguments,
            )

            print(f"TOOL RESULT: {result}")

            # Return the tool result to NVIDIA for a final response.
            follow_up = self.nvidia_client.chat.completions.create(
                model=self.nvidia_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                    {
                        "role": "assistant",
                        "content": message.content,
                        "tool_calls": [
                            {
                                "id": tool_call.id,
                                "type": "function",
                                "function": {
                                    "name": tool_name,
                                    "arguments": tool_call.function.arguments,
                                },
                            }
                        ],
                    },
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    },
                ],
                max_tokens=500,
                temperature=0.7,
            )

            return (
                follow_up.choices[0].message.content
                or str(result)
            )

        except Exception as e:
            print("NVIDIA API ERROR:", repr(e))
            return (
                "I'm unable to complete that request because "
                "the NVIDIA AI service is currently unavailable."
            )
