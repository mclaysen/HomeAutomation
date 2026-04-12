import json
import logging
import logging.config
from typing import List
from models.door_sensor import DoorSensorData
from models.sensorMappings import ModelMapping
from models.temp_sensor import TempSensorData
from models.water_sensor import WaterSensorData
from mqttHandlers.publisher import MqttPublisher
from mqttHandlers.subscriber import MqttSubcriber
from mqttHandlers.subscriberModel import Subscriber

class RTLSub:
    def __init__(self, ip : str, modelMappings : List[ModelMapping], publisher : MqttPublisher, logger: logging.Logger):
        self.logger = logger
        self.publisher=  publisher
        self.modelMappings = modelMappings
        self.ip = ip
        subscriberData = Subscriber(ip, 1883, "rtl_433/+/events/#", self.on_message)
        self.subscriber = MqttSubcriber(subscriberData, logger)

    def connect(self) -> None:
        self.logger.info("Connecting to RTL at %s", self.ip)
        self.subscriber.connect()
    
    def quit(self) -> None:
        self.subscriber.quit()

    def on_message(self, client, userdata, message) -> None:
        try:
            payload = message.payload.decode("utf-8")
            payload_obj = json.loads(payload)
            self.logger.debug(payload)
            if payload_obj["model"] == "Acurite-Tower":
                decodedpayload = TempSensorData.from_dict(json.loads(payload))
                tempModel = next(model for model in self.modelMappings if model.model == decodedpayload.model)
                if(tempModel is not None):
                    sensor = next(sensor for sensor in tempModel.sensors if sensor.id == decodedpayload.id)
                    if(sensor is not None):
                        self.publisher.publish("rtl_433/"+sensor.name,message.payload, 0, False)
                    else:
                        self.logger.warn("No sensor found for %s", decodedpayload.id)
            elif payload_obj["model"] == "Generic-Remote":
                decodedpayload = DoorSensorData.from_dict(json.loads(payload))
                doorModel = next(model for model in self.modelMappings if model.model == decodedpayload.model)
                if(doorModel is not None):
                    sensor = next(sensor for sensor in doorModel.sensors if sensor.id == decodedpayload.house_code)
                    if(sensor is not None):
                        self.publisher.publish("rtl_433/"+sensor.name,message.payload, 0, False)
                    else:
                        self.logger.warn("No sensor found for %s", decodedpayload.house_code)
            elif payload_obj["model"] == "Govee-Water":
                decodedpayload = WaterSensorData.from_dict(json.loads(payload))
                waterModel = next(model for model in self.modelMappings if model.model == decodedpayload.model)
                if(waterModel is not None):
                    sensor = next(sensor for sensor in waterModel.sensors if sensor.id == decodedpayload.id)
                    if(sensor is not None):
                        self.publisher.publish("rtl_433/"+sensor.name,message.payload, 0, False)
                    else:
                        self.logger.warn("No sensor found for %s", decodedpayload.id)
            else:
                self.logger.debug("Ignoring unsupported model: %s", payload_obj.get("model"))
        except Exception as e:
            self.logger.error("Error parsing payload for RTL message %s. Exception: %s", message.payload, e)
    


    
