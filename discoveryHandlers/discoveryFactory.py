from models.sensorTypes import SensorType

class DiscoveryFactory:
    def __init__(self, sensorType: SensorType) -> None:
        self.sensorType = sensorType

    def getDiscoveryObject(self) -> object:
        if self.sensorType == SensorType.TEMP_SENSOR:
            from discoveryHandlers.temperatureHumidityDiscovery import TempDiscovery
            return TempDiscovery()
        else:
            raise Exception("Invalid sensor type")
        
    
