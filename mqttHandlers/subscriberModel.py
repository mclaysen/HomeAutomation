from models.deviceType import DeviceType


class Subscriber:
    def __init__(self, deviceType: DeviceType, ip: str, port: int, topic: str):
        self.deviceType = deviceType
        self.ip = ip
        self.port = port
        self.topic = topic
        self.client = None
