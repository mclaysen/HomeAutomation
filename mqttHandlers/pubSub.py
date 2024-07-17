from abc import ABC, abstractmethod
from typing import Callable
from paho.mqtt.client import Client
import paho.mqtt.client as mqtt
import uuid
import logging
import logging.config
import time


class PubSub(ABC):
    def __init__(self, callback, topic : str | None, logger: logging.Logger):
        self.client = None
        self.clientId = str(uuid.uuid4())
        self.topic = topic
        self.logger = logger
        self.callback = callback

    @abstractmethod
    def connect(self) -> None:
        self.logger.info("test")
    

    def publish(self, topic, payload) -> None:
        if(self.client == None):
            raise Exception("MQTT client is null")
        
        self.client.publish(topic, payload)

    def _startSubscriber(self, ip: str, port: int) -> None:
        self.logger.info("Starting subscriber for %s", ip)
        if self.client is not None:
            try:
                self.client.connect(ip, port)
                self.client.loop_start()
            except TimeoutError:
                self.logger.error("Timeout connecting to %s", ip)
                time.sleep(15)
            except Exception as e:
                self.logger.error("Error connecting to %s. Exception: %s", ip, e)
        else:
            self.logger.error("Client is not connected")


    def on_connect(self, client : Client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        if(self.topic != None):
            client.subscribe(self.topic)
    
    def disconnect(self, client : Client, userdata, rc) -> None:
        self.logger.warn("Disconnecting")
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
        if self.client is not None:
            self.client.loop_stop()
            self.client.disconnect()

    def is_connected(self) -> bool:
        if self.client is not None:
            return self.client.is_connected()
        return False