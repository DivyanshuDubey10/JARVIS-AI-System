from core.tools import Tool
from modules.system import SystemHandler


class ToolManager:

    def __init__(self):
        self.tools = {}

        self.system = SystemHandler()

        self.register(
            Tool(
                name="open_app",
                description="Open a Windows application by name.",
                parameters={
                    "type": "object",
                    "properties": {
                        "app_name": {
                            "type": "string",
                            "description": "Name of the application to open."
                        }
                    },
                    "required": ["app_name"]
                },
                function=self.system.open_app
            )
        )

    def register(self, tool):
        self.tools[tool.name] = tool

    def get_tool(self, name):
        return self.tools.get(name)

    def get_all_tools(self):
        return list(self.tools.values())

    def execute(self, name, **kwargs):
        tool = self.get_tool(name)

        if tool is None:
            return f"Tool '{name}' was not found."

        try:
            return tool.execute(**kwargs)

        except Exception as e:
            return f"Tool '{name}' failed: {e}"