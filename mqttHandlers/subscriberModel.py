class Subscriber:
    def __init__(self, ip, port, topic) -> None:
        self.ip = ip
        self.port = port
        self.topic = topic
        self.client = None