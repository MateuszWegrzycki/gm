import RPi.GPIO as GPIO #Importing GPIO module
import paho.mqtt.client as mqtt #Importing Mosquitto Module
import time #Importing time to use delays
import random #Importing random to use generator of random numbers
 
 
GPIO.setmode(GPIO.BCM) #Deciding whether our GPIO pin numeration is BCM or BOARD
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Declaring 21 pin as INPUT with Pullup Resistor

 


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("127.0.0.1", 1883, 60)
 

 
# The activity after the interrupt on 21 pin
def interrupt_big_red_button(pin):
	client.publish('home-assistant/lottery/number', 'triggered'  )
	time.sleep(1)
	client.publish('home-assistant/lottery/number', 'disarmed'  )
	 
#Setup the interrupt on 21 pin with detection of falling edge 
GPIO.add_event_detect(21, GPIO.FALLING, callback = interrupt_big_red_button)
 
 
while True:
    time.sleep(1)

  

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
