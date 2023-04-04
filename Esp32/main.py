from time import sleep
from umqtt.simple import MQTTClient
from machine import Pin
import network
import I2C

pir_pin = Pin(14, Pin.IN)
touch = Pin(17, Pin.IN)

def knap():
    global touch_val
    touch_val = touch.value()
    print('Touch value:', touch_val)

def pir():
    global pir_val
    pir_val = pir_pin.value()
    print('PIR value:', pir_val)


station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("Gruppe5Wifi", "Wifi5Gruppe")

SERVER = '192.168.137.139'  # MQTT Server Address (Change to the IP address of your Pi)
CLIENT_ID = 'ESP32'
TOPIC = 'data'

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()   # Connect to MQTT broker

while True:
    try:
        pir()
        knap()
        I2C.ldr_read()
        msg = ('{0:1.0f},{1:1.0f},{2:d}'.format(pir_val, touch_val, I2C.value))
        client.publish(TOPIC, msg)  # Publish sensor data to MQTT topic
        print(msg)
            
    except OSError as e:
        print('Failed to read sensor.')
    sleep(0.5)

