from mqttHandelers.subcriberModel import Subscriber
from mqttHandlers.pubSub import PubSub

class FakeMqttSubscriber(PubSub):
    def __init__(self, callback, topic, logger):
        self.callback = callback
        self.topic = topic
        self.logger = logger
    
    def connect(self, client : Client, userdata, flags, rc) -> None: