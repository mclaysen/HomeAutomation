from models.door_sensor import DoorSensorData
from models.sensorMappings import Config
from models.sensorTypes import SensorType
import logging
from models.water_sensor import WaterSensorData
from mqttHandlers.messageHandler import MessageHandler
from models.temp_sensor import TempSensorData
from mqttHandlers.subscriber import MqttSubscriber
from mqttHandlers.subscriberModel import Subscriber
import json
from typing import TypeVar
from mqttHandlers.publisher import MqttPublisher


T = TypeVar('T')

class MessageHandlerFactory:
    def __init__(self, subscriberData: Subscriber, publisher: MqttPublisher, appSettings: Config, logger: logging.Logger):
        self.subscriberData = subscriberData
        self.appSettings = appSettings
        self.logger = logger
        self.publisher = publisher
        subscriber = MqttSubscriber(subscriberData, logger)
        subscriber.connect(self.on_message)

    def __create_message_handler(self, sensorType: SensorType) -> MessageHandler:
        if sensorType == SensorType.TEMP_SENSOR:
            return MessageHandler(self.subscriberData, self.appSettings, self.publisher, self.logger)
        else:
            raise ValueError(f"Unsupported sensor type: {sensorType}")
        
    def on_message(self, client, userdata, message) -> None:
        try:
            payload = message.payload.decode("utf-8")
            payload_obj = json.loads(payload)
            self.logger.debug(payload)



            match payload_obj["model"]:
                case "Acurite-Tower":
                    messageHander = self.__create_message_handler(SensorType.TEMP_SENSOR)
                    casted_payload = TempSensorData.from_dict(payload_obj)
                    messageHander.on_message(casted_payload)
                case "Generic-Remote":
                    messageHander = self.__create_message_handler(SensorType.DOOR_SENSOR)
                case "Govee-Water":
                    messageHander = self.__create_message_handler(SensorType.WATER_SENSOR)
                case _:
                    self.logger.warning("Unknown model: %s", payload_obj["model"])
                    return
        except Exception as e:
            self.logger.error("Error parsing payload. Exception: %s", e)