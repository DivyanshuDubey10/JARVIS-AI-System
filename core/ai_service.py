
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
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        self.tool_manager = ToolManager()
        self.max_tool_rounds = 5

    def generate(self, prompt):
        try:
            tool_definitions = self.tool_manager.get_tool_definitions()

            tools = [
                {
                    "type": "function",
                    "function": tool,
                }
                for tool in tool_definitions
            ]

            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]

            for round_number in range(self.max_tool_rounds + 1):
                response = self.nvidia_client.chat.completions.create(
                    model=self.nvidia_model,
                    messages=messages,
                    tools=tools,
                    max_tokens=500,
                    temperature=0.7,
                )

                message = response.choices[0].message

                if not message.tool_calls:
                    return (
                        message.content
                        or "NVIDIA returned an empty response."
                    )

                # Preserve the assistant's complete tool-call message.
                messages.append(message.model_dump(exclude_none=True))

                # Execute every tool requested in this response.
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name

                    print(f"\nAI TOOL CALL: {tool_name}")

                    try:
                        arguments = json.loads(
                            tool_call.function.arguments or "{}"
                        )

                        if not isinstance(arguments, dict):
                            raise ValueError(
                                "Tool arguments must be a JSON object."
                            )

                        print(f"Arguments: {arguments}")

                        result = self.tool_manager.execute(
                            tool_name,
                            **arguments,
                        )

                    except Exception as tool_error:
                        result = f"Tool execution failed: {tool_error}"
                        print(result)

                    print(f"TOOL RESULT: {result}")

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result),
                        }
                    )

            return (
                "I reached the maximum number of tool-execution rounds. "
                "Please try a simpler request."
            )

        except Exception as e:
            print("NVIDIA API ERROR:", repr(e))

            return (
                "I'm unable to complete that request because "
                "the NVIDIA AI service is currently unavailable."
            )
