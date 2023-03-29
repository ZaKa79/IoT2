from machine import Pin, SoftI2C 
import time

# Define I2C bus
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

# Define device address
device_address = 0x49

def ldr_read():
    #Read data from I2C bus
    global value
    data = i2c.readfrom(device_address, 2)
    value = int.from_bytes(data, "big")
    print("I2C data: ", value)
    

    