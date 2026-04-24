from discoveryHandlers.discoveryFactory import DiscoveryFactory
from models.sensorTypes import SensorType
import json
from models.sensorMappings import Config

def publish_discovery(client, appSettings : Config) -> None:
    tempDiscoveryFactory = DiscoveryFactory(SensorType.TEMP_SENSOR)
    doorDiscoveryFactory = DiscoveryFactory(SensorType.DOOR_SENSOR)

    for modelMapping in appSettings.ModelMappings:
        if(modelMapping.sensorType == SensorType.TEMP_SENSOR):
            for sensor in modelMapping.sensors:
                discoveryObject = tempDiscoveryFactory.getDiscoveryObject(sensor.name, str(sensor.id), None)
                discoveryTopic = discoveryObject.topic_for_discovery()
                discoveryPayload = discoveryObject.getDiscoveryPayload("rtl_433/"+sensor.name)
                client.publish(discoveryTopic, json.dumps(discoveryPayload), 1, True)
        elif(modelMapping.sensorType == SensorType.DOOR_SENSOR):
            for sensor in modelMapping.sensors:
                discoveryObject = doorDiscoveryFactory.getDiscoveryObject(sensor.name, str(sensor.id), modelMapping.model)
                discoveryTopic = discoveryObject.topic_for_discovery()
                discoveryPayload = discoveryObject.getDiscoveryPayload("rtl_433/"+sensor.name)
                client.publish(discoveryTopic, json.dumps(discoveryPayload), 1, True)