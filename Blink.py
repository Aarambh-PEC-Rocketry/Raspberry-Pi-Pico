from machine import Pin
from time import sleep
pin=machine.Pin(4,machine.Pin.OUT)
pin.value(1)
sleep(1)