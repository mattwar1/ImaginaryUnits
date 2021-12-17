import RPi.GPIO as GPIO
import time
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice,XBee64BitAddress

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600
COORDINATOR_ID = "0013A20040E441E5"

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
LED_GREEN = 19
LED_RED = 26

#set constans
SENSOR_MAX = 400
SENSOR_MIN = 2
LENGTH_OCCUPIED = 100
LENGTH_PARKING = 200

#init error variable
ERR = False

#set GPIO
def gpio_init():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
# set direction (IN / OUT)    
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_RED, GPIO.OUT)

def led_change(occupied):
    if not occupied:
        GPIO.output(LED_GREEN, GPIO.HIGH)
        GPIO.output(LED_RED, GPIO.LOW)
    elif occupied:
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(LED_RED, GPIO.HIGH)
    else:
        print("That shouldn't have happened\n")


#def sensor function# 
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

def main(DATA_TO_SEND):
    # print(" +--------------------------------------+")
    # print(" | XBee Python Library Send Data Sample |")
    # print(" +--------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)
    remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(COORDINATOR_ID))

    try:
        device.open()
        # Obtain the remote XBee device from the XBee network.
        # xbee_network = device.get_network()
        # print(xbee_network)
        # remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        # print(remote_device)
        if remote is None:
            print("Could not find the remote device")
            return None

        print("Sending data to %s >> %s..." % (COORDINATOR_ID, DATA_TO_SEND))
        device.send_data(remote, DATA_TO_SEND)
        
        # while True:
        #     print("Sending data to %s >> %s..." % ("0013A20040E441E5", DATA_TO_SEND))
        #     device.send_data(remote, DATA_TO_SEND)
        #     time.sleep(2)
        #     print("Success")     
    finally:
        if device is not None and device.is_open():
            print("XBee device is not connected, can't send the data")
            device.close()

# check i-times if measurment is stable
def chceck_measurment(i):
    a = 0
    b = i
    while(i > 0):
        a = a + distance()
        i = i - 1
    return  a / b



if __name__ == '__main__':
    gpio_init()
    try:
        while True:
            occupation_status = False
            error_staus = False
            led_change(occupation_status)
            ERR = False
            while(ERR!=True):
                time.sleep(1)
                a = distance()
                print ("Measured Distance = %.1f cm" % a)
                while True:
                    if(a <= SENSOR_MIN): 
                         if(error_staus == True):
                             break
                         elif(error_staus == False):
                            a = chceck_measurment(10)
                            if(a <= SENSOR_MIN):
                                print("To close")
                                error_staus = True
                                main("Error: to close")
                                print(error_staus)
                                break
                            else:
                                break
                    elif(a <= LENGTH_OCCUPIED):
                        if(occupation_status == True):
                            break
                        elif(occupation_status == False):
                            a = chceck_measurment(10)
                            #i = 10
                            #while(i > 0):
                            #    a = a + distance()
                            #    i = i - 1
                            #a = a / 10
                            if(a <= LENGTH_OCCUPIED):
                                occupation_status = True
                                led_change(occupation_status)
                                main("place occupied")
                                print ("Measured Distance = %.1f cm" % a)
                                print ( occupation_status)
                                break
                            else:
                                break

                    elif(SENSOR_MAX  > a > LENGTH_OCCUPIED):
                        if(occupation_status == False):
                            break
                        elif(occupation_status == True):
                            a = chceck_measurment(10)
                            if(a > LENGTH_OCCUPIED):
                                
                                occupation_status=False
                                led_change(occupation_status)
                                main("place not occupied")
                                print ("Measured Distance = %.1f cm" % a)
                                print (occupation_status)
                                break
                            else: 
                                break
                    elif(a > SENSOR_MAX):
                        if(error_staus == True):
                             break
                        elif(error_staus == False):
                            a = chceck_measurment(10)
                            if(a > SENSOR_MAX):
                                print("To far")
                                error_staus = True
                                main("Error: to far")
                                print(error_staus)
                                break
                            else:
                                break

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()




                    # dist = distance()
            # print ("Measured Distance = %.1f cm" % dist)
            # time.sleep(1.5)
        # Reset by pressing CTRL + C

                    # if(a <= SENSOR_MIN): 
                    #     if(error_staus == True):
                    #         break
                    #     elif(error_staus == False):
                    #         i = 10
                    #         while(i > 0):
                    #             a = a + distance()
                    #             i = i - 1
                    #         a = a / 10
                    #         if(a <= LENGTH_OCCUPIED):
                    #             occupation_status = True
                    #             led_change(occupation_status)
                    #             main("place occupied")
                    #             print ("Measured Distance = %.1f cm" % a)
                    #             print ( occupation_status)
                    #             break
                    #         else:
                    #             break