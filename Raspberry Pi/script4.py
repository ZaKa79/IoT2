import paho.mqtt.client as mqtt
from gpiozero import PWMLED
import sqlite3
from datetime import datetime
import time
import gps2

SERVER = '192.168.137.139'  # MQTT Server Address (Change to the IP address of your Pi)
TOPIC = 'data'
led = PWMLED(17, frequency=500) # GPIO pins connected to the RGB LED

#Opret database. Undlad hvis den findes. Connect til data.db
conn = sqlite3.connect('data.db')
c = conn.cursor() #make a cursor
c.execute("CREATE TABLE IF NOT EXISTS data (id integer PRIMARY KEY AUTOINCREMENT, datetime timestamp, lys int, latitude REAL, longitude REAL)") #creates the database 


# Callback function to handle MQTT message
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    split_list = payload.split(",")
    print("Received message: " + payload)
    split_list = [int(x) for x in split_list]

    gps2.gps_read()

    if split_list[2] < 3500:
        led.value = 0.1 #Led on 20%
        if split_list[0] == 1:
            led.value = 1
            
        elif split_list[1] == 1:
            led.value = 1
            end_time = time.time() + 4 #End time in 4s
            while time.time() < end_time: #Loop for 4s
                pass
    else:
        led.off()  # Turn off LED
        print("...")

    try:
        dt = datetime.now().strftime('%d-%m-%Y %H.%M.%S') #time and date
        lys = split_list[2]
        lat = 99
        lng = 99
        conn = sqlite3.connect('data.db')
        c = conn.cursor() #make a cursor        
        query = "INSERT INTO data (DateTime,lys, latitude, longitude) VALUES (?,?,?,?)" #setup for injection
        values = (dt,lys, lat, lng) # the values
        c.execute (query, values) #Udfør ovenstående og indsæt values der er defineret med 2 argumenter i linje 54
        conn.commit() #send values

    except sqlite3.Error as e:
        conn.rollback()
        print(f'Could not insert ! {e}')
        
    finally:
        conn.close()

# Set up MQTT client
client = mqtt.Client()
client.on_message = on_message
client.connect(SERVER)
client.subscribe(TOPIC)
# Loop to continuously listen for incoming messages
client.loop_forever()
