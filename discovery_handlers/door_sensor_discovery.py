from discovery_handlers.abstract_discovery_handler import AbstractDiscoveryHandler
from models.sensorTypes import SensorType


class DoorSensorDiscovery(AbstractDiscoveryHandler):
    def __init__(self, sensorName: str, sensorId: str, sensorModel: str) -> None:
        super().__init__(SensorType.DOOR_SENSOR, sensorName, sensorId, sensorModel)
        self.sensorName = sensorName.upper()
        self.sensorId = sensorId
        self.sensorModel = sensorModel
    
    def __getDeviceSoftware(self) -> str:
        if self.sensorModel is not None:
            return self.sensorModel
        else:
            return "Unknown Door Sensor"
        
    def __getCoverStatusObject(self) -> dict:
        name = self.sensorName + " Cover Status"
        if self.sensorModel ==  "Generic-Remote":
            return {
                "p": "event",
                "name": name,
                "value_template": "{{ '{ \"event_type\": \"cover_open\" }' if (value_json.cmd | int(0)) == 7 else '{}' }}",
                "event_types": ["cover_open"],
                "unique_id": self.getUniquePrefix("coverstate")
            }
        else:
            return {
                "p": "binary_sensor",
                "name": name,
                "device_class": "tamper",
                "value_template": "{{ value_json.cmd | int }}",
                "payload_on": 7,
                "payload_off": 8,
                "unique_id": self.getUniquePrefix("coverstate")
            }

    def getDiscoveryPayload(self, stateTopic: str) -> dict:
        payload = {
            "dev": {
                "ids": self.sensorId,
                "name": self.sensorName + " Door Sensor",
                "mf": "Golden Security",
                "mdl": "GS-WDS07",
                "sw": self.__getDeviceSoftware()
            },
            "o": self.getOriginInfo(),
            "cmps":
            {
                "doorStatus": {
                    "p": "binary_sensor",
                    "name": self.sensorName + " Door Status",
                    "device_class": "door",
                    "value_template": "{{ value_json.cmd | int }}",
                    "payload_on": 10,
                    "payload_off": 14,
                    "unique_id": self.getUniquePrefix("openstate")
                },
                "batteryStatus": {
                    "p": "event",
                    "name": self.sensorName + " Battery Status",
                    "value_template": "{{ '{ \"event_type\": \"battery_low\" }' if (value_json.cmd | int(0)) == 6 else '{}' }}",
                    "event_types": ["battery_low"],
                    "unique_id": self.getUniquePrefix("battery")
                },
                "coverStatus": self.__getCoverStatusObject(),
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