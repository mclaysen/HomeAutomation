import paho.mqtt.client as mqtt
from mqtt_handlers.subscriber_model import SubscriberModel, SecureSubscriberModel
from paho.mqtt.client import Client
import uuid
import logging
import logging.config
from mqtt_handlers.pub_sub import PubSub
from typing import Callable, Any

class SecureMqttSubscriber(PubSub):
    def __init__(self, subscriberData: SecureSubscriberModel, logger: logging.Logger) :
        super().__init__(subscriberData.deviceType, subscriberData.topic, logger)
        self.clientId = str(uuid.uuid4())
        self.client = None
        self.logger = logger
        self.username = subscriberData.username
        self.password = subscriberData.password
        self.subsciberData = subscriberData

    def connect(self, callback: Callable[[Any], None] = None) -> Client:
        if callback is not None:
            self.callback = callback
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, self.clientId, clean_session=False)
        if self.username is not None and self.password is not None:
            self.client.username_pw_set(
                username=self.username,
                password=self.password,
            )
        else:
            self.logger.warning("No username provided for subscriber %s", self.clientId)
            raise ValueError("Username is required for secure MQTT subscriber")

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.disconnect
        if self.callback is not None:
            self.client.on_message = self.callback
        else:
            self.logger.warning("No callback provided for subscriber %s", self.clientId)
        self.logger.info("Connecting to %s, client id %s", self.subsciberData.ip, self.clientId)
        self._startSubscriber(self.subsciberData.ip, self.subsciberData.port)
        return self.client

class MqttSubscriber(PubSub):
    def __init__(self, subscriberData: SubscriberModel, logger: logging.Logger) :
        super().__init__(subscriberData.deviceType, subscriberData.topic, logger)
        self.subsciberData = subscriberData
        self.clientId = str(uuid.uuid4())
        self.client = None
        self.logger = logger

    def connect(self, callback: Callable[[Any], None] = None) -> Client:
        if callback is not None:
            self.callback = callback
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, self.clientId, clean_session=False)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.disconnect
        if self.callback is not None:
            self.client.on_message = self.callback
        else:
            self.logger.warning("No callback provided for subscriber %s", self.clientId)
        self.logger.info("Connecting to %s, client id %s", self.subsciberData.ip, self.clientId)
        self._startSubscriber(self.subsciberData.ip, self.subsciberData.port)
        return self.client