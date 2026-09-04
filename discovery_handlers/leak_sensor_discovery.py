from discovery_handlers.abstract_discovery_handler import AbstractDiscoveryHandler
from models.sensor_types import SensorType


class LeakSensorDiscovery(AbstractDiscoveryHandler):
    def __init__(self, sensorName: str, sensorId: str) -> None:
        super().__init__(SensorType.LEAK_SENSOR, sensorName, sensorId, None)
        self.expireAfter = 180
        self.sensorName = sensorName.upper()
        self.sensorId = sensorId

    def getComponentTopicMap(self, defaultTopic: str) -> dict[str, str]:
        return {
            "leakStatus": defaultTopic + "/state/leak",
            "buttonPressed": defaultTopic + "/event/button",
        }

    def getDiscoveryPayload(self, stateTopic: str) -> dict:
        payload = {
            "dev": {
                "ids": self.sensorId,
                "name": self.sensorName + " Leak Sensor",
                "mf": "Govee",
                "mdl": "H5054",
            },
            "o": self.getOriginInfo(),
            "cmps": {
                "leakStatus": {
                    "p": "binary_sensor",
                    "name": self.sensorName + " Leak Status",
                    "device_class": "moisture",
                    "value_template": "{{ value_json.detect_wet | int }}",
                    "payload_on": 1,
                    "payload_off": 0,
                    "unique_id": self.getUniquePrefix("detect_wet"),
                },
                "readReceived": {
                    "p": "sensor",
                    "device_class": "timestamp",
                    "value_template": "{{ as_datetime(value_json.time) }}",
                    "unique_id": self.getUniquePrefix("readreceived"),
                    "name": self.sensorName + " Read Received",
                },
                "buttonPressed": {
                    "p": "event",
                    "name": self.sensorName + " Button Pressed",
                    "unique_id": self.getUniquePrefix("buttonpressed"),
                    "event_types": ["Button Press"],
                    "value_template": (
                        '{"event_type": "{{ value_json.event }}", '
                        '"id": {{ value_json.id }}, '
                        '"model": "{{ value_json.model }}", '
                        '"time": "{{ value_json.time }}"}'
                    ),
                },
            },
            "qos": 0,
        }
        return self.applyComponentTopicMap(payload, stateTopic)
