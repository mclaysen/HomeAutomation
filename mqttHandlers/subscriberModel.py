from models.deviceType import DeviceType


class Subscriber:
    def __init__(
        self,
        deviceType: DeviceType,
        ip: str,
        port: int,
        topic: str,
        username: str | None = None,
        password: str | None = None,
    ):
        self.deviceType = deviceType
        self.ip = ip
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password
        self.client = None
