from abc import ABC, abstractmethod
from models.sensor_types import SensorType

class AbstractDiscoveryHandler(ABC):
    def __init__(self, sensorType: SensorType, sensorName: str, sensorId: str, sensorModel: str | None = None) -> None:
        self.sensorType = sensorType
        self.sensorName = sensorName
        self.sensorId = sensorId
        self.sensorModel = sensorModel

    @abstractmethod
    def getDiscoveryPayload(self, stateTopic: str) -> dict:
        pass

    def getOriginInfo(self) -> dict:
        return {
            "name": "mclaysen - HomeAutomation",
            "sw": "1.0.0"
        }

    def topic_for_discovery(self) -> str:
        return "homeassistant/device/" + self.sensorName + "/" + self.sensorId + "/config"
    
    def getUniquePrefix(self, deviceClass: str) -> str:
        if(self.sensorType == SensorType.TEMP_SENSOR):
            type = "temperaturesensor"
        elif(self.sensorType == SensorType.DOOR_SENSOR):
            type = "doorsensor"
        elif(self.sensorType == SensorType.WATER_SENSOR):
            type = "watersensor"
        else:
            type = "unknownsensor"
        return self.sensorName + "_" + type + "_" + deviceClass