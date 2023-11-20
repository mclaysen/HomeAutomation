import json
import paho.mqtt.client as paho
import signal
import sys
import configparser
from models.temp_sensor import SensorData
from models.sensorMappings import Config
from publisher import MqttPublisher
from models.subscriber import Subscriber
from subscriber import MqttSubcriber

config = configparser.ConfigParser()
config.read('config.ini')

with open('config.json') as f:
    data = json.load(f)
    appsettings = Config.from_dict(data)

def on_message_dte(client, userdata, message):
    powerData = message.payload.decode("utf-8")
    decodedEnergyData = json.loads(powerData)
    print(decodedEnergyData)
    if "type" not in decodedEnergyData:
        homeassistantclient.publish("energy/meter/instant",powerData)
    else:
        homeassistantclient.publish("energy/meter/summary",powerData)

def on_message_rtl(client, userdata, message):
    payload = message.payload.decode("utf-8")
    decodedpayload = SensorData.from_dict(json.loads(payload))

    for sensor in appsettings.sensorMappings:
        if sensor.id == decodedpayload.id:
            homeassistantclient.publish("rtl_433/"+sensor.name,message.payload)
        
def connect_homeassistant() -> MqttPublisher:
    client = MqttPublisher()
    username = config.get('HOMEASSISTANT', 'USER')
    password = config.get('HOMEASSISTANT', 'PASSWORD')
    homeassistantip = appsettings.HOMEASSISTANT_IP
    print("connecting to home assistant", homeassistantip)
    client.connect(homeassistantip, username, password)
    return client

def connect_rtl(clientid):
    rtl_ip = appsettings.RTL_IP
    client = paho.Client(clientid)
    client.connect(rtl_ip, 1883)
    return client

homeassistantclient = connect_homeassistant()

dtesub = Subscriber(appsettings.DTE_IP, 2883, "event/metering/#", on_message_dte)
dtesubclient = MqttSubcriber(dtesub)
dtesubclient.connect()

rtlclient = connect_rtl("client-8")
rtlclient.on_message = on_message_rtl
rtlclient.subscribe("rtl_433/raspberrypi/events/#")
rtlclient.loop_forever()

def exit_gracefully(signum, frame):
    print("exiting")
    homeassistantclient.disconnect()
    dtesubclient.disconnect()

    rtlclient.disconnect()
    rtlclient.loop_stop()

    sys.exit(0)

signal.signal(signal.SIGTERM, exit_gracefully)
signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGQUIT, exit_gracefully)
