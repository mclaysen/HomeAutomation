from discovery_handlers.abstract_discovery_handler import AbstractDiscoveryHandler
from models.sensorTypes import SensorType

class LeakSensorDiscovery(AbstractDiscoveryHandler):
    def __init__(self, sensorName : str, sensorId: str) -> None:
        super().__init__(SensorType.WATER_SENSOR, sensorName, sensorId, None)
        self.expireAfter = 180
        self.sensorName = sensorName.upper()
        self.sensorId = sensorId

    def getDiscoveryPayload(self, stateTopic: str) -> dict:
        payload = {
            "dev": {
                "ids": self.sensorId,
                "name": self.sensorName + " Leak Sensor",
                "mf": "Govee",
                "mdl": "H5054"
            },
            "o": self.getOriginInfo(),
            "cmps":
            {
                "leakStatus": {
                    "p": "binary_sensor",
                    "name": self.sensorName + " Leak Status",
                    "device_class": "moisture",
                    "value_template": "{{ value_json.water_ok | int }}",
                    "payload_on": 0,
                    "payload_off": 1,
                    "unique_id": self.getUniquePrefix("water")
                },
                "readReceived": {
                    "p": "sensor",
                    "device_class": "timestamp",
                    "value_template": "{{ as_datetime(value_json.time) }}",
                    "unique_id": self.getUniquePrefix("readreceived"),
                    "name": self.sensorName + " Read Received"
                }
            },
            "qos": 0,
            "state_topic": stateTopic
        }
        return payload