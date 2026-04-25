import logging
from models.sensor_mappings import Config
from mqtt_handlers.subscriber_model import SubscriberModel
from typing import TypeVar
from mqtt_handlers.mqtt_publisher import MqttPublisher
from discovery_handlers.publish_discovery import publish_discovery

T = TypeVar('T')

class HomeAssistantMessageHandler:
    def __init__(self, subscriberData: SubscriberModel,  appSettings: Config,  publisher: MqttPublisher, logger: logging.Logger):
        self.appSettings = appSettings
        self.publisher = publisher
        self.logger = logger
        self.deviceType = subscriberData.deviceType

    def on_message(self, payload: str) -> None:
        self.logger.debug(payload)
        try:
            if payload == "online":
                publish_discovery(self.publisher, self.appSettings)
        except Exception as e:
            self.logger.error("Error handling message: %s", e)