import json
import signal
import sys
import configparser
import os
from log import MqttLogger
from models.sensorMappings import Config
from mqttHandlers.messageHandlers.messageHandlerFactory import MessageHandlerFactory
from mqttHandlers.publisher import MqttPublisher
from mqttHandlers.rtlSub import RTLSub
from mqttHandlers.subscriberModel import Subscriber
from mqttHandlers.subscriber import MqttSubscriber
from mqttHandlers.publisherModel import Publisher
from models.deviceType import DeviceType
from discoveryHandlers.publishDiscovery import publish_discovery

logger = MqttLogger("console_logger").getLogger()
config = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_index = os.path.join(current_dir, 'config.ini')
config_json = os.path.join(current_dir, 'config.json')

config.read(config_index)

with open(config_json) as f:
    data = json.load(f)
    appsettings = Config.from_dict(data)

def connect_homeassistant() -> MqttPublisher:
    username = config.get('HOMEASSISTANT', 'USER')
    password = config.get('HOMEASSISTANT', 'PASSWORD')
    homeassistantip = appsettings.HOMEASSISTANT_IP
    publiserData = Publisher(DeviceType.HOME_ASSISTANT, homeassistantip, 1883, username, password)
    client = MqttPublisher(publisherData=publiserData, logger=logger)
    logger.info("Connecting to Home Assistant at %s", homeassistantip)
    client.connect()
    return client

def on_ha_status(client, userdata, message):
    status = message.payload.decode("utf-8").strip().lower()
    logger.info("Home Assistant status: %s", status)
    if status == "online":
        publish_discovery(client, appsettings)

homeassistantclient = connect_homeassistant()
publish_discovery(homeassistantclient, appsettings)

dtesub = Subscriber(DeviceType.ENERGY_METER, appsettings.DTE_IP, 2883, "event/metering/#")
messageHandlerFactoryDte = MessageHandlerFactory(dtesub, homeassistantclient, appsettings, logger)

subscriberData = Subscriber(DeviceType.RF_433, appsettings.RTL_IP, 1883, "rtl_433/+/events/#")
messageHandlerFactoryRtl = MessageHandlerFactory(subscriberData, homeassistantclient, appsettings, logger)

ha_status_sub = Subscriber(DeviceType.HOME_ASSISTANT, appsettings.HOMEASSISTANT_IP, 1883, "homeassistant/status")
ha_status_client = MqttSubscriber(ha_status_sub, logger)
ha_status_client.connect(on_ha_status)

def exit_gracefully(signum, frame):
    print("exiting")
    homeassistantclient.quit()
    messageHandlerFactoryDte.close()
    messageHandlerFactoryRtl.close()

    sys.exit(0)

signal.signal(signal.SIGTERM, exit_gracefully)
signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGQUIT, exit_gracefully)

while True:
    pass