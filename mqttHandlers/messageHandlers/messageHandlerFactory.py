from models.door_sensor import DoorSensorData
from models.energy_data import EnergyData
from models.sensor_mappings import Config
import logging
from models.leak_sensor import WaterSensorData
from mqttHandlers.messageHandlers.rtlMessageHandler import RtlMessageHandler
from mqttHandlers.messageHandlers.energyMessageHandler import EnergyMessageHandler
from mqttHandlers.messageHandlers.homeAssistantHandler import HomeAssistantMessageHandler
from models.temp_sensor import TempSensorData
from mqttHandlers.mqtt_subscriber import MqttSubscriber
from mqttHandlers.subscriber_model import SubscriberModel
import json
from typing import TypeVar
from mqttHandlers.mqtt_publisher import MqttPublisher
from models.device_type import DeviceType
from mqttHandlers.ports.messageHandlerPort import MessageHandlerPort


T = TypeVar('T')

class MessageHandlerFactory:
    def __init__(self, subscriberData: SubscriberModel, publisher: MqttPublisher, appSettings: Config, logger: logging.Logger):
        self.subscriberData = subscriberData
        self.appSettings = appSettings
        self.logger = logger
        self.publisher = publisher
        self.subscriber = MqttSubscriber(subscriberData, logger)
        self.subscriber.connect(self.on_message)

    def __create_message_handler(self) -> MessageHandlerPort:
        if self.subscriberData.deviceType == DeviceType.RF_433:
            return RtlMessageHandler(self.subscriberData, self.appSettings, self.publisher, self.logger)
        elif self.subscriberData.deviceType == DeviceType.ENERGY_METER:
            return EnergyMessageHandler(self.subscriberData, self.appSettings, self.publisher, self.logger)
        elif self.subscriberData.deviceType == DeviceType.HOME_ASSISTANT:
            return HomeAssistantMessageHandler(self.subscriberData, self.appSettings, self.publisher, self.logger)
        else:
            raise ValueError(f"Unsupported sensor type: {self.subscriberData.deviceType}")

    def close(self):
        self.subscriber.quit()
        self.subscriber = None
        self.logger.info("Closed subscriber for device type: %s", self.subscriberData.deviceType)

    def on_message(self, client, userdata, message) -> None:
        try:
            payload = message.payload.decode("utf-8")
            self.logger.debug(payload)

            messageHander = self.__create_message_handler()
            casted_payload = None
            if self.subscriberData.deviceType == DeviceType.RF_433:
                payload_obj = json.loads(payload)
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
                payload_obj = json.loads(payload)
                casted_payload = EnergyData.from_dict(payload_obj)
            elif self.subscriberData.deviceType == DeviceType.HOME_ASSISTANT:
                casted_payload = str(payload.strip().lower())
            messageHander.on_message(casted_payload)

        except Exception as e:
            self.logger.error("Error parsing payload. Exception: %s", e)

        