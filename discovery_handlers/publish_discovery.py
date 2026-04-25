from discovery_handlers.discovery_factory import DiscoveryFactory
from models.sensor_types import SensorType
import json
from models.sensor_mappings import Config
from mqtt_handlers.mqtt_publisher import MqttPublisher

def publish_discovery(client : MqttPublisher, app_settings : Config) -> None:
    temp_discovery_factory = DiscoveryFactory(SensorType.TEMP_SENSOR)
    door_discovery_factory = DiscoveryFactory(SensorType.DOOR_SENSOR)

    for modelMapping in app_settings.ModelMappings:
        if(modelMapping.sensorType == SensorType.TEMP_SENSOR):
            for sensor in modelMapping.sensors:
                discovery_object = temp_discovery_factory.get_discovery_object(sensor.name, str(sensor.id), None)
                discovery_topic = discovery_object.topic_for_discovery()
                discovery_payload = discovery_object.getDiscoveryPayload("rtl_433/"+sensor.name)
                client.publish(discovery_topic, json.dumps(discovery_payload), 1, True)
        elif(modelMapping.sensorType == SensorType.DOOR_SENSOR):
            for sensor in modelMapping.sensors:
                discovery_object = door_discovery_factory.get_discovery_object(sensor.name, str(sensor.id), modelMapping.model)
                discovery_topic = discovery_object.topic_for_discovery()
                discovery_payload = discovery_object.getDiscoveryPayload("rtl_433/"+sensor.name)
                client.publish(discovery_topic, json.dumps(discovery_payload), 1, True)