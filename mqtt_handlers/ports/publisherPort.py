from abc import ABC
from mqttHandlers.pubSub import PubSub

class PublisherPort(PubSub, ABC):
    pass