from typing import Protocol

class PublisherPort(Protocol):
    def connect(self):
        ...