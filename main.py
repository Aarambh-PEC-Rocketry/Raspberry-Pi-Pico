from machine import Pin, I2C
from time import sleep
import sdcard
import uos
import BME280
import utime 
# PICO - Pins
# sda=Pin(16), scl=Pin(17)
pin = machine.Pin(20, machine.Pin.OUT)
pin.value(1)


sda = machine.Pin(14)
scl = machine.Pin(15)
i2c = machine.I2C(1, sda=sda, scl=scl, freq=400000)
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

sd = sdcard.SDCard(spi, cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

utime.sleep_ms(100)

def altitude(pressure, sl_pressure):
    press_altitude = 44330 * (1 - (pressure / sl_pressure) ** (1/5.255))
    return press_altitude


# Open the file we just created and read from it

while True:
    bme = BME280.BME280(i2c=i2c)
    temp = bme.temperature
    pres_str = bme.pressure  # Assuming 'pressure' is in the format "XXXX.XXhPa"
    
    # Convert pressure value to float and extract numeric value
    pres_value = float(pres_str[:-3])
    
    # Assuming sea-level pressure is 1013.25 hPa, you can adjust this value
    pressure_altitude = altitude(pres_value, 1013.25)
    with open("/sd/test01.txt", "a") as file:
        file.write("Temperature: {}  Pressure: {}  Pressure Altitude: {}\r\n".format(temp, pres_str, pressure_altitude))
        print("Line Saved: Temperature: {}  Pressure: {}  Pressure Altitude: {}\r\n".format(temp, pres_str, pressure_altitude))        
        utime.sleep_ms(100)


    
#    sleep(0.5)
