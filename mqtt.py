import json
import signal
import sys
import configparser
from log import MqttLogger
from models.temp_sensor import SensorData
from models.sensorMappings import Config
from publisher import MqttPublisher
from models.subscriber import Subscriber
from subscriber import MqttSubcriber
from models.energyData import EnergyData, EnergyType

logger = MqttLogger("console_logger").getLogger()
config = configparser.ConfigParser()
config.read('config.ini')

with open('config.json') as f:
    data = json.load(f)
    appsettings = Config.from_dict(data)

def on_message_dte(client, userdata, message):
    powerData = message.payload.decode("utf-8")

    decodedEnergyData = EnergyData.from_dict(json.loads(powerData))
    logger.info(powerData)
    if decodedEnergyData.type == EnergyType.INSTANT:
        homeassistantclient.publish("energy/meter/instant",powerData)
    else:
        homeassistantclient.publish("energy/meter/summary",powerData)

def on_message_rtl(client, userdata, message):
    payload = message.payload.decode("utf-8")
    decodedpayload = SensorData.from_dict(json.loads(payload))
    logger.info(payload)
    for sensor in appsettings.sensorMappings:
        if sensor.id == decodedpayload.id:
            homeassistantclient.publish("rtl_433/"+sensor.name,message.payload)
        
def connect_homeassistant() -> MqttPublisher:
    client = MqttPublisher()
    username = config.get('HOMEASSISTANT', 'USER')
    password = config.get('HOMEASSISTANT', 'PASSWORD')
    homeassistantip = appsettings.HOMEASSISTANT_IP
    logger.info("Connecting to Home Assistant at %s", homeassistantip)
    client.connect(homeassistantip, username, password)
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
    homeassistantclient.disconnect()
    dtesubclient.quit()
    rtlsubclient.quit()

    sys.exit(0)

signal.signal(signal.SIGTERM, exit_gracefully)
signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGQUIT, exit_gracefully)

while True:
    pass





