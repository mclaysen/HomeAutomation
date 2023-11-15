import json
import paho.mqtt.client as paho
import signal
import sys
import configparser
from models.temp_sensor import SensorData

config = configparser.ConfigParser()
config.read('config.ini')

with open('config.json') as f:
    appsettings = json.load(f)

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
    print(decodedpayload.id)
    if decodedpayload.id==5161:
        homeassistantclient.publish("rtl_433/basement",message.payload)
    elif(decodedpayload.id==15881):
        homeassistantclient.publish("rtl_433/main_floor",message.payload)
    elif(decodedpayload.id==8386):
        homeassistantclient.publish("rtl_433/attic",message.payload)
    elif(decodedpayload.id==30409):
        homeassistantclient.publish("rtl_433/door_sensor",message.payload)
        
def connect_homeassistant(clientid):
    homeassistantip="192.168.86.78"
    print("connecting to home assistant", homeassistantip)
    homeassistantclient = paho.Client(clientid)
    username = config.get('HOMEASSISTANT', 'USER')
    password = config.get('HOMEASSISTANT', 'PASSWORD')
    homeassistantclient.username_pw_set(username=username,password=password)
    homeassistantclient.connect(homeassistantip)
    return homeassistantclient

def connect_dte(clientid):
    client= paho.Client(clientid)
    dte_ip = appsettings.get("DTE_IP")
    client.connect(dte_ip, 2883)
    return client

def connect_rtl(clientid):
    rtl_ip = appsettings.get("RTL_IP")
    client = paho.Client(clientid)
    client.connect(rtl_ip, 1883)
    return client

homeassistantclient = connect_homeassistant("client-5")

dteclient = connect_dte("client-7")
dteclient.on_message=on_message_dte
dteclient.subscribe("event/metering/#")
dteclient.loop_start()

rtlclient = connect_rtl("client-8")
rtlclient.on_message = on_message_rtl
rtlclient.subscribe("rtl_433/raspberrypi/events/#")
rtlclient.loop_forever()

def exit_gracefully(signum, frame):
    print("exiting")
    homeassistantclient.disconnect()
    dteclient.disconnect()
    dteclient.loop_stop()

    rtlclient.disconnect()
    rtlclient.loop_stop()

    sys.exit(0)

signal.signal(signal.SIGTERM, exit_gracefully)
signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGQUIT, exit_gracefully)
