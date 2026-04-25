from models.sensorTypes import SensorType
import discovery_handlers.abstract_discovery_handler as abstract_discovery_handler
from discovery_handlers.temperature_humidity_discovery import TemperatureHumidityDiscovery
from discovery_handlers.door_sensor_discovery import DoorSensorDiscovery

class DiscoveryFactory:
    def __init__(self, sensorType: SensorType) -> None:
        self.sensorType = sensorType

    def get_discovery_object(self, sensorName: str, sensorId: str, sensorModel: str | None) -> abstract_discovery_handler.AbstractDiscoveryHandler:
        if self.sensorType == SensorType.TEMP_SENSOR:
            return TemperatureHumidityDiscovery(sensorName, sensorId)
        elif self.sensorType == SensorType.DOOR_SENSOR:
            return DoorSensorDiscovery(sensorName, sensorId, sensorModel)
        else:
            raise Exception("Invalid sensor type")
        
    
