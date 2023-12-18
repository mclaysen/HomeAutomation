import paho.mqtt.client as mqtt
from models.subscriber import Subscriber
from paho.mqtt.client import Client
import uuid
import logging
import logging.config
class MqttSubcriber:
    def __init__(self, subscriberData: Subscriber, logger: logging.Logger) -> None:
        self.subsciberData = subscriberData
        self.clientId = str(uuid.uuid4())
        self.client = None
        self.logger = logger

    def connect(self) -> Client:
        self.client = mqtt.Client(self.clientId)
        self.client.on_message = self.subsciberData.callback
        self.logger.info("Connecting to %s", self.subsciberData.ip)
        self.client.connect(self.subsciberData.ip, self.subsciberData.port)
        self.client.subscribe(self.subsciberData.topic)
        self.client.loop_start()
        return self.client

    def disconnect(self) -> None:
        self.logger.info("Disconnecting from %s", self.subsciberData.ip)
        if self.client is not None:
            self.logger.info("Stopping loop")
            self.client.loop_stop()
            self.client.disconnect()

    def __del__(self):
        self.disconnect()