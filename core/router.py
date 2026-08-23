from modules.system import SystemHandler
from modules.browser import BrowserHandler
from modules.system_info import SystemInfoHandler
from modules.ai import AIHandler


class CommandRouter:

    def __init__(self):

        self.handlers = [
            SystemHandler(),
            BrowserHandler(),
            SystemInfoHandler(),
        ]

        self.ai = AIHandler()

    def handle(self, command, history=None):

        for handler in self.handlers:

            result = handler.handle(command)

            if result is not None:
                return result

        return self.ai.handle(command, history)