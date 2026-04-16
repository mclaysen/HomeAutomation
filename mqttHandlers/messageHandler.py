import json
import logging
from mqttHandlers import subscriberModel as Subscriber

class MessageHandler[T]:
    def __init__(self, subscriberData: Subscriber, logger: logging.Logger):
        self.subscriber = Subscriber(subscriberData.ip, subscriberData.port, subscriberData.topic, subscriberData.callback)
        self.logger = logger
    
    def on_message(self, payload) -> None:
        try:
            decodedpayload = T.from_dict(json.loads(payload))
            out_payload = json.dumps(decodedpayload.__dict__)
            self.logger.debug(out_payload)
            tempModel = next(model for model in self.modelMappings if model.model == decodedpayload.model)
            if(tempModel is not None):
                sensor = next(sensor for sensor in tempModel.sensors if sensor.id == decodedpayload.id)
                if(sensor is not None):
                    self.publisher.publish("rtl_433/"+sensor.name,out_payload, 0, False)
                else:
                    self.logger.warning("No sensor found for %s", decodedpayload.id)
        except Exception as e:
            self.logger.error("Error handling message: %s", e)