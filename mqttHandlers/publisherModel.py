class Publisher:
    def __init__(self, ip, port, username, password) -> None:
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.client = None