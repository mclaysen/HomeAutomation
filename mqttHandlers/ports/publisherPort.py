from typing import Protocol
from mqttHandlers.pubSub import PubSub

class PublisherPort(PubSub, Protocol):
    def connect(self):
        ...