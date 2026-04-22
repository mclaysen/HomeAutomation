from models.door_sensor import DoorSensorData
from models.energyData import EnergyData
from models.sensorMappings import Config
import logging
from models.water_sensor import WaterSensorData
from mqttHandlers.messageHandlers.rtlMessageHandler import RtlMessageHandler
from mqttHandlers.messageHandlers.energyMessageHandler import EnergyMessageHandler
from models.temp_sensor import TempSensorData
from mqttHandlers.subscriber import MqttSubscriber
from mqttHandlers.subscriberModel import Subscriber
import json
from typing import TypeVar
from mqttHandlers.publisher import MqttPublisher
from models.deviceType import DeviceType
from mqttHandlers.ports.messageHandlerPort import MessageHandlerPort


T = TypeVar('T')

class MessageHandlerFactory:
    def __init__(self, subscriberData: Subscriber, publisher: MqttPublisher, appSettings: Config, logger: logging.Logger):
        self.subscriberData = subscriberData
        self.appSettings = appSettings
        self.logger = logger
        self.publisher = publisher
        subscriber = MqttSubscriber(subscriberData, logger)
        subscriber.connect(self.on_message)

    def __create_message_handler(self) -> MessageHandlerPort:
        if self.subscriberData.deviceType == DeviceType.RF_433:
            return RtlMessageHandler(self.subscriberData, self.appSettings, self.publisher, self.logger)
        elif self.subscriberData.deviceType == DeviceType.ENERGY_METER:
            return EnergyMessageHandler(self.subscriberData, self.appSettings, self.publisher, self.logger)
        else:
            raise ValueError(f"Unsupported sensor type: {self.subscriberData.deviceType}")
        
    def on_message(self, client, userdata, message) -> None:
        try:
            payload = message.payload.decode("utf-8")
            payload_obj = json.loads(payload)
            self.logger.debug(payload)

            messageHander = self.__create_message_handler()
            casted_payload = None
            if self.subscriberData.deviceType == DeviceType.RF_433:
                match payload_obj["model"]:
                    case "Acurite-Tower":
                        casted_payload = TempSensorData.from_dict(payload_obj)
                    case "Generic-Remote":
                        casted_payload = DoorSensorData.from_dict(payload_obj)
                    case "Govee-Water":
                        casted_payload = WaterSensorData.from_dict(payload_obj)
                    case _:
                        self.logger.warning("Unknown model: %s", payload_obj["model"])
                        return
            elif self.subscriberData.deviceType == DeviceType.ENERGY_METER:
                casted_payload = EnergyData.from_dict(payload_obj)
            elif self.subscriberData.deviceType == DeviceType.HOME_ASSISTANT:
                return
            messageHander.on_message(casted_payload)

        except Exception as e:
            self.logger.error("Error parsing payload. Exception: %s", e)

        