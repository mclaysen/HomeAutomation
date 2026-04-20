class Subscriber:
    def __init__(self, ip, port, topic):
        self.ip = ip
        self.port = port
        self.topic = topic
        self.client = None
