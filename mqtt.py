import json
import signal
import sys
import configparser
import os
from log import MqttLogger
from models.sensorMappings import Config
from models.sensorTypes import SensorType
from mqttHandlers.publisher import MqttPublisher
from mqttHandlers.rtlSub import RTLSub
from mqttHandlers.subscriberModel import Subscriber
from mqttHandlers.subscriber import MqttSubcriber
from models.energyData import EnergyData, EnergyType
from mqttHandlers.publisherModel import Publisher
from discoveryHandlers.discoveryFactory import DiscoveryFactory


logger = MqttLogger("console_logger").getLogger()
config = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_index = os.path.join(current_dir, 'config.ini')
config_json = os.path.join(current_dir, 'config.json')

config.read(config_index)

with open(config_json) as f:
    data = json.load(f)
    appsettings = Config.from_dict(data)

def on_message_dte(client, userdata, message):
    try:
        powerData = message.payload.decode("utf-8")

        decodedEnergyData = EnergyData.from_dict(json.loads(powerData))
        logger.debug(powerData)
        if decodedEnergyData.type == EnergyType.INSTANT:
            homeassistantclient.publish("energy/meter/instant",powerData, 0, False)
        else:
            homeassistantclient.publish("energy/meter/summary",powerData, 0, False)
    except Exception as e:
        logger.error("Error parsing payload for DTE. Exception: %s", e)

def connect_homeassistant() -> MqttPublisher:
    
    username = config.get('HOMEASSISTANT', 'USER')
    password = config.get('HOMEASSISTANT', 'PASSWORD')
    homeassistantip = appsettings.HOMEASSISTANT_IP
    publiserData = Publisher(homeassistantip, 1883, username, password)
    client = MqttPublisher(publisherData=publiserData, logger=logger)
    logger.info("Connecting to Home Assistant at %s", homeassistantip)
    client.connect()
    return client

def publish_discovery(client, appSettings):
    discoveryFactory = DiscoveryFactory(SensorType.TEMP_SENSOR)

    tempDiscovery = discoveryFactory.getDiscoveryObject("basement", "5161")

    tempPayload = tempDiscovery.getDiscoveryPayload("rtl_433/basement")
    tempTopic = tempDiscovery.topic_for_discovery()
    client.publish(tempTopic, json.dumps(tempPayload), 1, True)

def on_ha_status(client, userdata, message):
    status = message.payload.decode("utf-8").strip().lower()
    logger.info("Home Assistant status: %s", status)
    if status == "online":
        publish_discovery(client, appsettings)

homeassistantclient = connect_homeassistant()
publish_discovery(homeassistantclient, appsettings)

dtesub = Subscriber(appsettings.DTE_IP, 2883, "event/metering/#", on_message_dte)
dtesubclient = MqttSubcriber(dtesub, logger)
logger.info("Connecting to DTE at %s", appsettings.DTE_IP)
dtesubclient.connect()

rtlSub = RTLSub(appsettings.RTL_IP, appsettings.ModelMappings, homeassistantclient, logger)
rtlSub.connect()

ha_status_sub = Subscriber(appsettings.HOMEASSISTANT_IP, 1883, "homeassistant/status", on_ha_status)
ha_status_client = MqttSubcriber(ha_status_sub, logger)
ha_status_client.connect()

def exit_gracefully(signum, frame):
    print("exiting")
    homeassistantclient.quit()
    dtesubclient.quit()
    rtlSub.quit()

    sys.exit(0)

signal.signal(signal.SIGTERM, exit_gracefully)
signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGQUIT, exit_gracefully)

while True:
    pass