class Subscriber:
    def __init__(self, ip, port, topic, callback) -> None:
        self.ip = ip
        self.port = port
        self.topic = topic
        self.callback = callback
        self.client = None