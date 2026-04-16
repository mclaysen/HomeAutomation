from typing import Protocol

class MessageHandlerPort[T](Protocol):
    def on_message(self, payload) -> list[str]:
        ...