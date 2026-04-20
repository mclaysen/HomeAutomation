import logging

from models.sensorMappings import Config
from mqttHandlers.subscriberModel import Subscriber
from typing import TypeVar
from mqttHandlers.publisher import MqttPublisher


T = TypeVar('T')

class MessageHandler:
    def __init__(self, subscriberData: Subscriber,  appSettings: Config,  publisher: MqttPublisher, logger: logging.Logger):
        self.subscriber = Subscriber(subscriberData.ip, subscriberData.port, subscriberData.topic)
        self.appSettings = appSettings
        self.publisher = publisher
        self.logger = logger
        
    
    def on_message(self, payload: T) -> None:
        try:
            self.logger.debug(payload)
            tempModel = next(model for model in self.appSettings.ModelMappings if model.model == payload.model)
            if(tempModel is not None):
                sensor = next(sensor for sensor in tempModel.sensors if sensor.id == payload.id)
                if(sensor is not None):
                    self.publisher.publish("rtl_433/"+sensor.name,payload, 0, False)
                else:
                    self.logger.warning("No sensor found for %s", payload.id)
        except Exception as e:
            self.logger.error("Error handling message: %s", e)