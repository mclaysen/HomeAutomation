from typing import Protocol, TypeVar

T = TypeVar('T')

class MessageHandlerPort(Protocol):
    def on_message(self, payload: T) -> None:
        ...