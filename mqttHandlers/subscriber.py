import paho.mqtt.client as mqtt
from mqttHandlers.subscriberModel import Subscriber
from paho.mqtt.client import Client
import uuid
import logging
import logging.config
from mqttHandlers.pubSub import PubSub

class MqttSubcriber(PubSub):
    def __init__(self, subscriberData: Subscriber, logger: logging.Logger) :
        super().__init__(subscriberData.callback, subscriberData.topic, logger)
        self.subsciberData = subscriberData
        self.clientId = str(uuid.uuid4())
        self.client = None
        self.logger = logger

    def connect(self) -> Client:
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, self.clientId, clean_session=False)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.disconnect
        self.client.on_message = self.subsciberData.callback
        self.logger.info("Connecting to %s, client id %s", self.subsciberData.ip, self.clientId)
        self._startSubscriber(self.subsciberData.ip, self.subsciberData.port)
        return self.client