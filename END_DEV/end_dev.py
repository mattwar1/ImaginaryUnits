
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice,XBee64BitAddress
import time
import RPi.GPIO as GPIO

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

DATA_TO_SEND = b'0101011'


def main():
    print(" +--------------------------------------+")
    print(" | XBee Python Library Send Data Sample |")
    print(" +--------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)
    remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20040E441E5"))

    try:
        device.open()

        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        print(xbee_network)
        # remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        # print(remote_device)
        if remote is None:
            print("Could not find the remote device")
            exit(1)

        print("Sending data to %s >> %s..." % ("0013A20040E441E5", DATA_TO_SEND))

        while True:
            print("Sending data to %s >> %s..." % ("0013A20040E441E5", DATA_TO_SEND))
            device.send_data(remote, DATA_TO_SEND)
            time.sleep(2)
            print("Success")
        

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()

 

 


 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()