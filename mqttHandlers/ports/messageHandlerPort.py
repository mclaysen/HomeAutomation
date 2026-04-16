from typing import Protocol

class MessageHandlerPort(Protocol):
    def on_message(self, payload) -> list[str]:
        ...