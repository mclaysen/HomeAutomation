from models.sensorTypes import SensorType
import discoveryHandlers.abstractDiscoveryHandler as abstractDiscoveryHandler
from discoveryHandlers.temperatureHumidityDiscovery import TempHumidityDiscovery

class DiscoveryFactory:
    def __init__(self, sensorType: SensorType) -> None:
        self.sensorType = sensorType

    def getDiscoveryObject(self, sensorName: str, sensorId: str) -> abstractDiscoveryHandler.AbstractDiscoveryHandler:
        if self.sensorType == SensorType.TEMP_SENSOR:
            return TempHumidityDiscovery(sensorName, sensorId)
        else:
            raise Exception("Invalid sensor type")
        
    
