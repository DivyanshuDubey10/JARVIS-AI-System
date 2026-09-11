import ollama
from core.tool_manager import ToolManager


class AIService:

    def __init__(self):
        self.model = "qwen3:4b-instruct"

        self.client = ollama.Client(
            host="http://127.0.0.1:11434"
        )

        self.tool_manager = ToolManager()

    def generate(self, prompt):

        tools = []

        for tool in self.tool_manager.get_all_tools():

            tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            })

        try:

            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                tools=tools
            )

            if response.message.tool_calls:

                for tool_call in response.message.tool_calls:

                    tool_name = tool_call.function.name
                    arguments = tool_call.function.arguments

                    result = self.tool_manager.execute(
                        tool_name,
                        **arguments
                    )

                    return result

            return response.message.content

        except Exception as e:

            print("OLLAMA ERROR:", repr(e))
            return f"AI Error: {e}"