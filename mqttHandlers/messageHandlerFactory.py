from models.door_sensor import DoorSensorData
from models.sensorTypes import SensorType
import logging
from models.water_sensor import WaterSensorData
from mqttHandlers.messageHandler import MessageHandler
from models.temp_sensor import TempSensorData
from mqttHandlers.ports.messageHandlerPort import MessageHandlerPort
from mqttHandlers.subscriberModel import Subscriber
import json

class MessageHandlerFactory:
    def __init__(self, subscriberData: Subscriber, logger: logging.Logger):
        self.subscriberData = subscriberData
        self.logger = logger

    def create_message_handler[T](self, sensorType: SensorType) -> MessageHandlerPort[T]:
        if sensorType == SensorType.TEMP:
            return MessageHandler[TempSensorData](self.subscriberData, self.logger)
        else:
            raise ValueError(f"Unsupported sensor type: {sensorType}")
        
    def on_message(self, message) -> None:
        try:
            payload = message.payload.decode("utf-8")
            payload_obj = json.loads(payload)
            self.logger.debug(payload)

            match payload_obj["model"]:
                case "Acurite-Tower":
                    messageHander = self.create_message_handler(SensorType.TEMP_SENSOR)[TempSensorData]
                case "Generic-Remote":
                    messageHander = self.create_message_handler(SensorType.DOOR_SENSOR)[DoorSensorData]
                case "Govee-Water":
                    messageHander = self.create_message_handler(SensorType.WATER_SENSOR)[WaterSensorData]
                case _:
                    self.logger.warning("Unknown model: %s", payload_obj["model"])
                    return
            messageHander.on_message(payload)
        except Exception as e:
            self.logger.error("Error parsing payload. Exception: %s", e)