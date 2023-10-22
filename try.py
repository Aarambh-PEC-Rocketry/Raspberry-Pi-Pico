from machine import Pin, I2C
from time import sleep
import sdcard
import uos
import BME280
import utime
import math
# PICO - Pins
# sda=Pin(16), scl=Pin(17)
pin = machine.Pin(20, machine.Pin.OUT)
pin.value(1)


sda = machine.Pin(14)
scl = machine.Pin(15)
cs = machine.Pin(9,machine.Pin.OUT)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10),
                  mosi=machine.Pin(11),
                  miso=machine.Pin(12))



# Mount filesystem


utime.sleep_ms(100)

def bme(sda,scl):
    try:
        i2c = machine.I2C(1, sda=sda, scl=scl, freq=400000)
        bme = BME280.BME280(i2c=i2c)
        temp = bme.temperature
        pres_str = bme.pressure 
        pres_value = float(pres_str[:-3])
        pressure_altitude = altitude(pres_value, 1013.25)
        print(temp,"-Temp", pres_value,"-pressure")
    except:
        return math.nan

def altitude(pressure, sl_pressure):
    press_altitude = 44330 * (1 - (pressure / sl_pressure) ** (1/5.255))
    return press_altitude

def sdcard(cs ,spi,temp,pres_str, pressure_altitude):
    try:
        
        sd = sdcard.SDCard(spi, cs)
        vfs = uos.VfsFat(sd)
        uos.mount(vfs, "/sd")
        with open("/sd/test01.txt", "a") as file:
            file.write("Temperature: {}  Pressure: {}  Pressure Altitude: {}\r\n".format(temp, pres_str, pressure_altitude))
            print("Line Saved: Temperature: {}  Pressure: {}  Pressure Altitude: {}\r\n".format(temp, pres_str, pressure_altitude))
            
    except:
        return "Value not written"








# Open the file we just created and read from it

while True:
    bme(sda,scl)
    sdcard(cs ,spi,temp,pres_str, pressure_altitude)
    



    
#    sleep(0.5)

