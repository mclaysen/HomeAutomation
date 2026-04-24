import json
import logging
from models.sensorMappings import Config
from mqttHandlers.ports.publisherPort import PublisherPort
from mqttHandlers.subscriberModel import Subscriber
from typing import TypeVar

T = TypeVar('T')

class RtlMessageHandler:
    def __init__(self, subscriberData: Subscriber,  appSettings: Config,  publisher: PublisherPort, logger: logging.Logger):
        self.appSettings = appSettings
        self.publisher = publisher
        self.logger = logger
        self.deviceType = subscriberData.deviceType
        
    
    def on_message(self, payload: T) -> None:
        self.logger.debug(payload)
        try:
            tempModel = next(model for model in self.appSettings.ModelMappings if model.model == payload.model)
            if(tempModel is not None):
                sensor = next(sensor for sensor in tempModel.sensors if sensor.id == payload.id)
                if(sensor is not None):
                    self.publisher.publish("rtl_433/"+sensor.name, json.dumps(payload.to_dict()), 0, False)
                else:
                    self.logger.warning("No sensor found for %s", payload.id)
        except Exception as e:
            self.logger.error("Error handling message: %s", e)