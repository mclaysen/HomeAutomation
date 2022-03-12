import time
from turtle import home
import paho.mqtt.client as paho
broker="192.168.2.190"

#define callback

homeassistant="192.168.86.78"
print("connecting to home assistant", homeassistant)
homeassistantclient = paho.Client("client-1")
homeassistantclient.username_pw_set("mqtt","snapple15")
homeassistantclient.connect(homeassistant)


def on_message(client, userdata, message):
    #time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))

    powerData = message.payload.decode("utf-8")

    homeassistantclient.publish("energy/meter",powerData, retain= True)#publish    



client= paho.Client("client-1") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")

######Bind function to callback
client.on_message=on_message
#####
#print("connecting to dte ",broker)
client.connect(broker, 2883)#connect



#client.loop_start() #start loop to process received messages
#print("subscribing ")
client.subscribe("event/metering/#")#subscribe
#time.sleep(2)
#print("publishing ")

#time.sleep(4)
#client.disconnect() #disconnect
#client.loop_stop() #stop loop
client.loop_forever()