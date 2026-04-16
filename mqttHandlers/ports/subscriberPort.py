from multiprocessing.dummy.connection import Client
from typing import Any, Callable, Protocol

class SubscriberPort[T](Protocol):
    def connect(self, callback: Callable[[Any], None]) -> Client:
        ...