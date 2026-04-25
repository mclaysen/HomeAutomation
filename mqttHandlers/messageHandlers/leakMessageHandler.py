import logging
from models.energy_type import EnergyType
from models.sensor_mappings import Config
from mqttHandlers.subscriberModel import Subscriber
from typing import TypeVar
from mqttHandlers.publisher import MqttPublisher
import json

T = TypeVar('T')

class EnergyMessageHandler:
    def __init__(self, subscriberData: Subscriber,  appSettings: Config,  publisher: MqttPublisher, logger: logging.Logger):
        self.appSettings = appSettings
        self.publisher = publisher
        self.logger = logger
        self.deviceType = subscriberData.deviceType

    def on_message(self, payload: T) -> None:
        self.logger.debug(payload)
        try:
            if payload.type == EnergyType.INSTANT:
                self.publisher.publish("energy/meter/instant",json.dumps(payload.to_dict()), 0, False)
            else:
                self.publisher.publish("energy/meter/summary",json.dumps(payload.to_dict()), 0, False)
        except Exception as e:
            self.logger.error("Error parsing payload for DTE. Exception: %s", e)