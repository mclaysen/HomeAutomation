from models.device_type import DeviceType


class Publisher:
    def __init__(self, deviceType: DeviceType, ip: str, port: int, username: str, password: str) -> None:
        self.deviceType = deviceType
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.client = None