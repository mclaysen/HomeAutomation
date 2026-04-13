from models.sensorTypes import SensorType
import discoveryHandlers.abstractDiscoveryHandler as abstractDiscoveryHandler
from discoveryHandlers.temperatureHumidityDiscovery import TempHumidityDiscovery
from discoveryHandlers.doorSensorDiscovery import DoorSensorDiscovery

class DiscoveryFactory:
    def __init__(self, sensorType: SensorType) -> None:
        self.sensorType = sensorType

    def getDiscoveryObject(self, sensorName: str, sensorId: str, sensorModel: str | None) -> abstractDiscoveryHandler.AbstractDiscoveryHandler:
        if self.sensorType == SensorType.TEMP_SENSOR:
            return TempHumidityDiscovery(sensorName, sensorId)
        elif self.sensorType == SensorType.DOOR_SENSOR:
            return DoorSensorDiscovery(sensorName, sensorId, sensorModel)
        else:
            raise Exception("Invalid sensor type")
        
    
