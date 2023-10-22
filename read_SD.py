import machine
import sdcard
import uos

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(1, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10),
                  mosi=machine.Pin(11),
                  miso=machine.Pin(12))
# Initialize SD card
sd = sdcard.SDCard(spi, cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

x= input("Do you want to Read[R] or Clear[C]:")
if (x=="C" or x=="c"):
    with open("/sd/test01.txt", "w")as file :
        data = file.write("")
        print("The Data Log has been Cleared !!")
elif (x=="R" or x=="r"):
# Open the file we just created and read from it
    with open("/sd/test01.txt", "r") as file:
        data = file.read()
        print(data)
else:
    print("Invalid Command")