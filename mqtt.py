import json
import signal
import sys
import configparser
import os
from log import MqttLogger
from models.temp_sensor import TempSensorData
from models.door_sensor import DoorSensorData
from models.sensorMappings import Config
from publisher import MqttPublisher
from models.subscriber import Subscriber
from subscriber import MqttSubcriber
from models.energyData import EnergyData, EnergyType
from models.publisher import Publisher

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
            homeassistantclient.publish("energy/meter/instant",powerData)
        else:
            homeassistantclient.publish("energy/meter/summary",powerData)
    except Exception as e:
        logger.error("Error parsing payload for DTE. Exception: %s", e)

def on_message_rtl(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        payload_obj = json.loads(payload)
        logger.debug(payload)
        if payload_obj["model"] == "Acurite-Tower":
            decodedpayload = TempSensorData.from_dict(json.loads(payload))
            tempModel = next(model for model in appsettings.ModelMappings if model.model == decodedpayload.model)
            if(tempModel is not None):
                sensor = next(sensor for sensor in tempModel.sensors if sensor.id == decodedpayload.id)
                if(sensor is not None):
                    homeassistantclient.publish("rtl_433/"+sensor.name,message.payload)
                else:
                    logger.warn("No sensor found for %s", decodedpayload.id)
        elif payload_obj["model"] == "Generic-Remote":
            decodedpayload = DoorSensorData.from_dict(json.loads(payload))
            doorModel = next(model for model in appsettings.ModelMappings if model.model == decodedpayload.model)
            if(doorModel is not None):
                sensor = next(sensor for sensor in doorModel.sensors if sensor.id == decodedpayload.house_code)
                if(sensor is not None):
                    homeassistantclient.publish("rtl_433/"+sensor.name,message.payload)
                else:
                    logger.warn("No sensor found for %s", decodedpayload.house_code)

    except Exception as e:
        logger.error("Error parsing payload for RTL message %s. Exception: %s", message.payload, e)
    
def connect_homeassistant():
    
    username = config.get('HOMEASSISTANT', 'USER')
    password = config.get('HOMEASSISTANT', 'PASSWORD')
    homeassistantip = appsettings.HOMEASSISTANT_IP
    publiserData = Publisher(homeassistantip, 1883, username, password)
    client = MqttPublisher(publisherData=publiserData)
    logger.info("Connecting to Home Assistant at %s", homeassistantip)
    client.connect()
    return client

homeassistantclient = connect_homeassistant()

dtesub = Subscriber(appsettings.DTE_IP, 2883, "event/metering/#", on_message_dte)
dtesubclient = MqttSubcriber(dtesub, logger)
logger.info("Connecting to DTE at %s", appsettings.DTE_IP)
dtesubclient.connect()

rtlsub = Subscriber(appsettings.RTL_IP, 1883, "rtl_433/raspberrypi/events/#", on_message_rtl)
rtlsubclient = MqttSubcriber(rtlsub, logger)
logger.info("Connecting to RTL at %s", appsettings.RTL_IP)
rtlsubclient.connect()

def exit_gracefully(signum, frame):
    print("exiting")
    homeassistantclient.quit()
    dtesubclient.quit()
    rtlsubclient.quit()

    sys.exit(0)

signal.signal(signal.SIGTERM, exit_gracefully)
signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGQUIT, exit_gracefully)

while True:
    pass





