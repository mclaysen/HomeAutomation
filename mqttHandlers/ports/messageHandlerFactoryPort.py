from typing import Protocol
from models.sensorTypes import SensorType
from mqttHandlers.ports.messageHandlerPort import MessageHandlerPort

class MessageHandlerFactoryPort(Protocol):
    def create_message_handler[T](self, sensorType: SensorType) -> MessageHandlerPort[T]:
        ...
    def on_message(self, client, userdata, message) -> None:
        ...