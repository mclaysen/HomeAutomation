from turtle import home
import paho.mqtt.client as paho

def on_message(client, userdata, message):
    print("received message =",str(message.payload.decode("utf-8")))
    powerData = message.payload.decode("utf-8")
    homeassistantclient.publish("energy/meter",powerData, retain= True)

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

homeassistantclient = connect_homeassistant("client-1")
rtlclient = connect_dte("client-1")
rtlclient.on_message=on_message
rtlclient.subscribe("event/metering/#")
rtlclient.loop_forever()