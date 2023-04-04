import serial
import time
import pynmea2


def gps_read():
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    newdata=ser.readline().decode("unicode_escape")

    if newdata[0:6] == "$GPRMC":
        newmsg=pynmea2.parse(newdata)
        lat=newmsg.latitude
        lng=newmsg.longitude
        print(lat, lng)


