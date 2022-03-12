from turtle import home
import json
import paho.mqtt.client as paho

def on_message_dte(client, userdata, message):
    powerData = message.payload.decode("utf-8")
    homeassistantclient.publish("energy/meter",powerData, retain= True)

def on_message_rtl(client, userdata, message):
    tempData = message.payload.decode("utf-8")
    decodedTempData =json.loads(tempData)
    if decodedTempData["id"]==5161:
        homeassistantclient.publish("rtl_433/basement",message.payload)#publish

def connect_homeassistant(clientid):
    homeassistantip="192.168.86.78"
    print("connecting to home assistant", homeassistantip)
    homeassistantclient = paho.Client(clientid)
    homeassistantclient.username_pw_set("mqtt","snapple15")
    homeassistantclient.connect(homeassistantip)
    return homeassistantclient

def connect_dte(clientid):
    client= paho.Client(clientid)
    dte_ip="192.168.2.190"
    client.connect(dte_ip, 2883)
    return client

def connect_rtl(clientid):
    rtl_ip = "localhost"
    client = paho.Client(clientid)
    client.connect(rtl_ip, 1883)
    return client

homeassistantclient = connect_homeassistant("client-1")

dteclient = connect_dte("client-1")
dteclient.on_message=on_message_dte
dteclient.subscribe("event/metering/#")
dteclient.loop_start()

rtlclient = connect_rtl("client-1")
rtlclient.on_message = on_message_rtl
rtlclient.subscribe("rtl_433/localhost/events")
rtlclient.loop_forever()