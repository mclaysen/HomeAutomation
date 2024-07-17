import uuid
import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
from mqttHandlers.publisherModel import Publisher
from mqttHandlers.pubSub import PubSub
import logging
import logging.config

class MqttPublisher(PubSub):
    def __init__(self, publisherData: Publisher, logger: logging.Logger) -> None:
        super().__init__(None, None, logger)
        self.clientId = str(uuid.uuid4())
        self.client = None
        self.publisherData = publisherData

    def connect(self) -> None :
        self.client = mqtt.Client(self.clientId, clean_session=False)
        self.client.username_pw_set(username=self.publisherData.username,password=self.publisherData.password)
        self.client.connect(self.publisherData.ip, self.publisherData.port)
        self.client.on_disconnect = self.disconnect
        self.client.on_connect = self._startSubscriber(self.publisherData.ip, self.publisherData.port)