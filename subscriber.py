import paho.mqtt.client as mqtt
from models.subscriber import Subscriber
from paho.mqtt.client import Client
import uuid
import logging
import logging.config
import time
class MqttSubcriber:
    def __init__(self, subscriberData: Subscriber, logger: logging.Logger) -> None:
        self.subsciberData = subscriberData
        self.clientId = str(uuid.uuid4())
        self.client = None
        self.logger = logger

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client : Client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(self.subsciberData.topic)

    def connect(self) -> Client:
        self.client = mqtt.Client(self.clientId)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.disconnect
        self.client.on_message = self.subsciberData.callback
        self.logger.info("Connecting to %s", self.subsciberData.ip)
        self.client.connect(self.subsciberData.ip, self.subsciberData.port)
        self.client.loop_start()
        return self.client

    def disconnect(self, client : Client, userdata, rc) -> None:
        self.logger.warn("Disconnecting from %s", self.subsciberData.ip)
        if self.client is not None:
            self.logger.info("Stopping loop")
            self.client.loop_stop()
            self.client.disconnect()

            while True:
                time.sleep(15)
                try:
                    self.logger.info("Reconnecting")
                    self.client.reconnect()
                    self.connect()
                    break
                except Exception as e:
                    self.logger.error("Error reconnecting. Exception: %s", e)
    
    def quit(self) -> None:
        self.logger.info("Stopping loop")
        if self.client is not None:
            self.client.loop_stop()
            self.client.disconnect()

    def __del__(self):
        self.quit()