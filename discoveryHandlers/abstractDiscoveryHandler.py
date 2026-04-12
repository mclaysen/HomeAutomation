from abc import ABC, abstractmethod
from models.sensorTypes import SensorType


class AbstractDiscoveryHandler(ABC):
    def __init__(self, sensorType: SensorType, sensorName: str, sensorId: str) -> None:
        self.sensorType = sensorType
        self.sensorName = sensorName
        self.sensorId = sensorId

    @abstractmethod
    def getDiscoveryPayload(self, stateTopic: str) -> dict:
        pass

    def topic_for_discovery(self) -> str:
        return "homeassistant/device/" + self.sensorName + "/" + self.sensorId + "/config"
    
    def getUniquePrefix(self, type: str) -> str:
        if(self.sensorType == SensorType.TEMP_SENSOR):
            type = "temperature"
        elif(self.sensorType == SensorType.DOOR_SENSOR):
            type = "door"
        elif(self.sensorType == SensorType.WATER_SENSOR):
            type = "water"
        else:
            type = "unknown"
        return type + "_" + self.sensorName + "_" + type