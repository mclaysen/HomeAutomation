from discoveryHandlers import abstractDiscoveryHandler
from models.sensorTypes import SensorType

class TempHumidityDiscovery(abstractDiscoveryHandler.AbstractDiscoveryHandler):
    def __init__(self, sensorName : str, sensorId: str) -> None:
        super().__init__(SensorType.TEMP_SENSOR, sensorName, sensorId)
        self.expireAfter = 180
        self.sensorName = sensorName
        self.sensorId = sensorId

    def getDiscoveryPayload(self, stateTopic: str) -> dict:
        payload = {
            "dev": {
                "ids": self.sensorId,
                "name": self.sensorName,
                "mf": "Acurite",
                "mdl": "Acurite-Tower"
            },
            "o": {
                "name": "mclaysen - HomeAutomation",
                "sw": "1.0.0"
            },
            "cmps":
            {
                "temperature": {
                    "p": "sensor",
                    "name": self.sensorName + " Temperature",
                    "device_class": "temperature",
                    "unit_of_measurement": "°C",
                    "value_template": "{{ value_json.temperature_C | float }}",
                    "unique_id": self.getUniquePrefix("temperature"),
                    "expire_after": self.expireAfter
                },
                "humidity": {
                    "p": "sensor",
                    "name": self.sensorName + " Humidity",
                    "unit_of_measurement": "%",
                    "device_class": "humidity",
                    "value_template": "{{ value_json.humidity | float }}",
                    "unique_id": self.getUniquePrefix("humidity"),
                    "expire_after": self.expireAfter
                },
                "batteryStatus": {
                    "p": "binary_sensor",
                    "name": self.sensorName + " Battery Status",
                    "device_class": "battery",
                    "value_template": "{{ value_json.battery_ok | number }}",
                    "payload_on": 1,
                    "payload_off": 0,
                    "unique_id": self.getUniquePrefix("battery")
                },
                "readReceived": {
                    "p": "sensor",
                    "device_class": "timestamp",
                    "value_template": "{{ as_datetime(value_json.time).isoformat() }}",
                    "unique_id": self.getUniquePrefix("read_received"),
                    "name": self.sensorName + " Read Received"
                }
            },
            "qos": 0,
            "state_topic": stateTopic
        }
        return payload