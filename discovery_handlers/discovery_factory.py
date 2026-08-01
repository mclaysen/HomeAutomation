import discovery_handlers.abstract_discovery_handler as abstract_discovery_handler
from discovery_handlers.door_sensor_discovery import DoorSensorDiscovery
from discovery_handlers.leak_sensor_discovery import LeakSensorDiscovery
from discovery_handlers.temperature_humidity_discovery import (
    TemperatureHumidityDiscovery,
)
from models.sensor_types import SensorType


class DiscoveryFactory:
    def get_discovery_object(
        self,
        sensorType: SensorType,
        sensorName: str,
        sensorId: str,
        sensorModel: str | None,
    ) -> abstract_discovery_handler.AbstractDiscoveryHandler:
        if sensorType == SensorType.TEMP_SENSOR:
            return TemperatureHumidityDiscovery(sensorName, sensorId)
        elif sensorType == SensorType.DOOR_SENSOR:
            return DoorSensorDiscovery(sensorName, sensorId, sensorModel)
        elif sensorType == SensorType.LEAK_SENSOR:
            return LeakSensorDiscovery(sensorName, sensorId)
        else:
            raise Exception("Invalid sensor type")
