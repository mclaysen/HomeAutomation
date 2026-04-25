from multiprocessing.dummy.connection import Client
from typing import Any
from mqtt_handlers.pub_sub import PubSub
from typing import Callable


class FakeMqttSubscriber(PubSub):

    @property
    def messages(self) -> list[str]:
        return self._messages

    def __init__(self, callback, topic, logger):
        self._messages = []
        self.callback = callback
        self.topic = topic
        self.logger = logger

    def callback(self, client, userdata, message):
        self.messages.append(message.payload.decode())

    def connect(self, callback: Callable[[Any], None] = None) -> Client:
        if callback is not None:
            self.callback = callback
        else:
            self.callback = self.callback
        self.logger.info("Fake subscriber connected to topic %s", self.topic)
        return None

class FakeMqttPublisher(PubSub):

    def __init__(self, logger):
        self._published_messages = []
        self.logger = logger

    @property
    def published_messages(self) -> list[tuple[str, str, int, bool]]:
        return self._published_messages

    def publish(self, topic, payload, qos, retain) -> None:
        self._published_messages.append((topic, payload, qos, retain))
        self.logger.info("Fake publisher published message to topic %s: %s", topic, payload)

    def connect(self, callback: Callable[[Any], None] = None) -> Client:
        if callback is not None:
            self.callback = callback
        else:
            self.callback = self.callback
        self.logger.info("Fake subscriber connected to topic %s", self.topic)
        return None