import logging
from models.sensorMappings import Config
from mqttHandlers.subscriberModel import Subscriber
from typing import TypeVar
from mqttHandlers.publisher import MqttPublisher
from discovery_handlers.publish_discovery import publish_discovery

T = TypeVar('T')

class HomeAssistantMessageHandler:
    def __init__(self, subscriberData: Subscriber,  appSettings: Config,  publisher: MqttPublisher, logger: logging.Logger):
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