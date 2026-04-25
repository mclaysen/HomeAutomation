from typing import Protocol
from models.sensor_types import SensorType
from mqtt_handlers.ports.message_handler_port import MessageHandlerPort

class MessageHandlerFactoryPort(Protocol):
    def create_message_handler[T](self, sensorType: SensorType) -> MessageHandlerPort[T]:
        ...
    def on_message(self, client, userdata, message) -> None:
        ...