class Logger:

    def __init__(self, logging_enabled = True):
        self._logging_enabled = logging_enabled

    def log(self, message):
        if self._logging_enabled:
            print(message)