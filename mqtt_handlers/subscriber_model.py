from models.device_type import DeviceType


class SubscriberModel:
    def __init__(
        self,
        deviceType: DeviceType,
        ip: str,
        port: int,
        topic: str,
    ):
        self.deviceType = deviceType
        self.ip = ip
        self.port = port
        self.topic = topic
        self.client = None

class SecureSubscriberModel(SubscriberModel):
    def __init__(
        self,
        deviceType: DeviceType,
        ip: str,
        port: int,
        topic: str,
        username: str,
        password: str
    ):
        super().__init__(deviceType, ip, port, topic)
        self.username = username
        self.password = password
        self._check_credentials()

    def _check_credentials(self):
        if self.username is None or self.username == "":
            self.logger.warning("No username provided for subscriber %s", self.clientId)
            raise ValueError("Username is required for secure MQTT subscriber")
        if self.password is None:
            self.logger.warning("No password provided for subscriber %s", self.clientId)
            raise ValueError("Password is required for secure MQTT subscriber")