import uuid
import paho.mqtt.client as mqtt
from mqtt_handlers.publisher_model import PublisherModel
from mqtt_handlers.ports.publisher_port import PublisherPort
import logging
import logging.config

class MqttPublisher(PublisherPort):
    def __init__(self, publisherData: PublisherModel, logger: logging.Logger) -> None:
        super().__init__(publisherData.deviceType, None, logger)
        self.clientId = str(uuid.uuid4())
        self.client = None
        self.publisherData = publisherData

    def connect(self) -> None :
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, self.clientId, clean_session=False)
        self.client.username_pw_set(username=self.publisherData.username,password=self.publisherData.password)
        self.client.on_disconnect = self.disconnect
        self._startSubscriber(self.publisherData.ip, self.publisherData.port)