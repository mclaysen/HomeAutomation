from typing import Any, Callable, Protocol
from mqttHandlers.pubSub import PubSub

class SubscriberPort[T](PubSub, Protocol):
    def connect(self) -> None:
        ...
    def define_callback(self, callback: Callable[[Any], None]) -> None:
        ...