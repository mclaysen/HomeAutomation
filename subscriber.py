import paho.mqtt.client
from models.subscriber import Subscriber

class MqttSubcriber:
    def __init__(self, subscriberData : Subscriber) -> None:
        self.subsciberData = subscriberData
        self.client = None

    def connect(self) -> None:
        self.client = paho.mqtt.client.Client("client-001")
        self.client.on_message = self.subsciberData.callback
        self.client.connect(self.subsciberData.ip, self.subsciberData.port)
        self.client.subscribe(self.subsciberData.topic)
        self.client.loop_start()

    def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def __del__(self):
        self.disconnect()