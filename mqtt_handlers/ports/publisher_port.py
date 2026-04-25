from abc import ABC
from mqtt_handlers.pub_sub import PubSub

class PublisherPort(PubSub, ABC):
    pass