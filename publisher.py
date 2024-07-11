import uuid
import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
from models.publisher import Publisher
import time

class MqttPublisher:
    def __init__(self, publisherData: Publisher) -> None:
        self.clientId = str(uuid.uuid4())
        self.client = None
        self.publisherData = publisherData

    def connect(self) -> None :
        self.client = mqtt.Client(self.clientId, clean_session=False)
        self.client.username_pw_set(username=self.publisherData.username,password=self.publisherData.password)
        self.client.connect(self.publisherData.ip, self.publisherData.port)
        self.client.on_disconnect = self.disconnect
        self.client.loop_start()

    def publish(self, topic, payload) -> None:
        if(self.client == None):
            raise Exception("MQTT client is null")
        
        self.client.publish(topic, payload)

    def disconnect(self, client : Client, userdata, rc) -> None:
        if self.client is not None:
            self.client.loop_stop()
            self.client.disconnect()

            while True:
                time.sleep(15)
                try:
                    self.client.reconnect()
                    self.connect()
                    break
                except Exception as e:
                    print("Error reconnecting. Exception: %s", e)
    
    def quit(self) -> None: 
        if self.client is not None:
            self.client.loop_stop()
            self.client.disconnect()

    def is_connected(self) -> bool:
        if self.client is not None:
            return self.client.is_connected()
        return False