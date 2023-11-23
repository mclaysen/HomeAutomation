import uuid
import paho.mqtt.client as mqtt

class MqttPublisher:
    def __init__(self) -> None:
        self.clientId = str(uuid.uuid4())
        self.client = None

    def connect(self, ip, username, password) -> None :
        self.client = mqtt.Client(self.clientId)
        self.client.username_pw_set(username=username,password=password)
        self.client.connect(ip)

    def publish(self, topic, payload) -> None:
        if(self.client == None):
            raise Exception("MQTT client not connected")
        self.client.publish(topic, payload)

    def disconnect(self) -> None:
        self.client.disconnect()
