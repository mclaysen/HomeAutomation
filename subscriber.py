import paho.mqtt.client as mqtt
from models.subscriber import Subscriber
from paho.mqtt.client import Client
import uuid
import logging

class MqttSubcriber:
    def __init__(self, subscriberData: Subscriber) -> None:
        self.subsciberData = subscriberData
        self.clientId = str(uuid.uuid4())
        self.client = None

    def connect(self) -> None:
        self.client = mqtt.Client(self.clientId)
        self.client.on_message = self.subsciberData.callback
        self.client.connect(self.subsciberData.ip, self.subsciberData.port)
        self.client.subscribe(self.subsciberData.topic)
        self.client.loop_start()

    def disconnect(self) -> None:
        if self.client is not None:
            self.client.loop_stop()
            self.client.disconnect()

    def __del__(self):
        self.disconnect()