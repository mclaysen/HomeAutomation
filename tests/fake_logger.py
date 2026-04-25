from logging import Logger

class FakeLogger(Logger):
    def __init__(self):
        self.logs = []
        self.disabled = True

    def info(self, message, *args):
        self.logs.append((message, args))

    def error(self, message, *args):
        self.logs.append((message, args))