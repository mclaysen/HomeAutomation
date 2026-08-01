import json

from discovery_handlers.discovery_factory import DiscoveryFactory
from models.sensor_mappings import Config
from models.sensor_types import SensorType
from mqtt_handlers.mqtt_publisher import MqttPublisher


def publish_discovery(
    client: MqttPublisher,
    app_settings: Config,
    discovery_factory: DiscoveryFactory,
) -> None:

    for modelMapping in app_settings.ModelMappings:
        if modelMapping.sensorType == SensorType.TEMP_SENSOR:
            for sensor in modelMapping.sensors:
                discovery_object = discovery_factory.get_discovery_object(
                    SensorType.TEMP_SENSOR, sensor.name, str(sensor.id), None
                )
                discovery_topic = discovery_object.topic_for_discovery()
                discovery_payload = discovery_object.getDiscoveryPayload(
                    "rtl_433/" + sensor.name
                )
                client.publish(discovery_topic, json.dumps(discovery_payload), 1, True)
        elif modelMapping.sensorType == SensorType.LEAK_SENSOR:
            for sensor in modelMapping.sensors:
                discovery_object = discovery_factory.get_discovery_object(
                    SensorType.LEAK_SENSOR, sensor.name, str(sensor.id), None
                )
                discovery_topic = discovery_object.topic_for_discovery()
                discovery_payload = discovery_object.getDiscoveryPayload(
                    "rtl_433/leak_sensor/" + sensor.name
                )
                client.publish(discovery_topic, json.dumps(discovery_payload), 1, True)
        elif modelMapping.sensorType == SensorType.DOOR_SENSOR:
            for sensor in modelMapping.sensors:
                discovery_object = discovery_factory.get_discovery_object(
                    SensorType.DOOR_SENSOR,
                    sensor.name,
                    str(sensor.id),
                    modelMapping.model,
                )
                discovery_topic = discovery_object.topic_for_discovery()
                discovery_payload = discovery_object.getDiscoveryPayload(
                    "rtl_433/" + sensor.name
                )
                client.publish(discovery_topic, json.dumps(discovery_payload), 1, True)
