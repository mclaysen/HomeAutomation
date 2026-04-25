from models.door_sensor import DoorSensor
from models.energy_data import EnergyData
from models.sensor_mappings import Config
import logging
from models.leak_sensor import LeakSensor
from mqtt_handlers.message_handlers.generic_rtl_message_handler import GenericRtlMessageHandler
from mqtt_handlers.message_handlers.energy_message_handler import EnergyMessageHandler
from mqtt_handlers.message_handlers.home_assistant_handler import HomeAssistantMessageHandler
from models.temp_sensor import TempSensor
from mqtt_handlers.mqtt_subscriber import MqttSubscriber, SecureMqttSubscriber
from mqtt_handlers.subscriber_model import SubscriberModel, SecureSubscriberModel
import json
from typing import TypeVar
from mqtt_handlers.mqtt_publisher import MqttPublisher
from models.device_type import DeviceType
from mqtt_handlers.ports.message_handler_port import MessageHandlerPort
from mqtt_handlers.message_handlers.leak_sensor_handler import LeakSensorHandler

T = TypeVar('T')

class MessageHandlerFactory:
    def __init__(self, subscriberData: SubscriberModel, publisher: MqttPublisher, appSettings: Config, logger: logging.Logger):
        self.subscriberData = subscriberData
        self.appSettings = appSettings
        self.logger = logger
        self.publisher = publisher
        if isinstance(subscriberData, SecureSubscriberModel):
            self.subscriber = SecureMqttSubscriber(subscriberData, logger)
        else:
            self.subscriber = MqttSubscriber(subscriberData, logger)
        self.subscriber.connect(self.on_message)

    def __create_message_handler(self, preferred_device_type: DeviceType | None = None) -> MessageHandlerPort:
        device_type = preferred_device_type if preferred_device_type is not None else self.subscriberData.deviceType
        if device_type == DeviceType.GENERIC_RF_433:
            return GenericRtlMessageHandler(self.subscriberData, self.appSettings, self.publisher, self.logger)
        elif device_type == DeviceType.ENERGY_METER:
            return EnergyMessageHandler(self.subscriberData, self.appSettings, self.publisher, self.logger)
        elif device_type == DeviceType.HOME_ASSISTANT:
            return HomeAssistantMessageHandler(self.subscriberData, self.appSettings, self.publisher, self.logger)
        elif device_type == DeviceType.LEAK_SENSOR:
            return LeakSensorHandler(self.subscriberData, self.appSettings, self.publisher, self.logger)
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
            preferred_device_type : DeviceType | None = None
            casted_payload = None
            if self.subscriberData.deviceType == DeviceType.GENERIC_RF_433:
                payload_obj = json.loads(payload)
                match payload_obj["model"]:
                    case "Acurite-Tower":
                        casted_payload = TempSensor.from_dict(payload_obj)
                    case "Generic-Remote":
                        casted_payload = DoorSensor.from_dict(payload_obj)
                    case "Govee-Water":
                        casted_payload = LeakSensor.from_dict(payload_obj)
                        preferred_device_type = DeviceType.LEAK_SENSOR
                    case _:
                        self.logger.warning("Unknown model: %s", payload_obj["model"])
                        return
            elif self.subscriberData.deviceType == DeviceType.ENERGY_METER:
                payload_obj = json.loads(payload)
                casted_payload = EnergyData.from_dict(payload_obj)
            elif self.subscriberData.deviceType == DeviceType.HOME_ASSISTANT:
                casted_payload = str(payload.strip().lower())
            messageHandler = self.__create_message_handler(preferred_device_type)
            messageHandler.on_message(casted_payload)

        except Exception as e:
            self.logger.error("Error parsing payload. Exception: %s", e)

        