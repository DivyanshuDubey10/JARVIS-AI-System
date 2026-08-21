from modules.system import SystemHandler
from modules.browser import BrowserHandler
from modules.system_info import SystemInfoHandler
from modules.ai import AIHandler


class CommandRouter:

    def __init__(self, timer_callback=None):

        self.handlers = [
            SystemHandler(timer_callback),
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

    def start_timer(self, seconds):

        system_handler = self.handlers[0]

        system_handler.start_timer(seconds)