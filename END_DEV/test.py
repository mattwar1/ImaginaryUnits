import RPi.GPIO as GPIO
import time


#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
LED_GREEN = 10
LED_RED = 9

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

if __name__ == '__main__':
    gpio_init()
    try:
        while True:
            occupation_status = False
            led_change(occupation_status)
            ERR = False
            while(ERR!=True):
                time.sleep(1)
                a = distance()
                print("Pobrałem dane\n")
                while True:

                    if(a<=LENGTH_OCCUPIED):
                        if(occupation_status==True):
                            print("Status bez zmian\n")
                            break
                        elif(occupation_status==False):
                            i = 5
                            while(i>0):
                                a = a + distance()
                                i=i-1
                            a = a/5
                            if(a<=LENGTH_OCCUPIED):
                                occupation_status=True
                                led_change(occupation_status)
                                #send changes
                                print ("Measured Distance = %.1f cm" % a)
                                print ( occupation_status)
                                break
                            else:
                                break

                    elif(a>LENGTH_OCCUPIED):
                        if(occupation_status==False):
                            break
                        elif(occupation_status==True):
                            j = 5
                            while(j>0):
                                a = a + distance()
                                j = j-1
                            a = a/5
                            if(a>LENGTH_OCCUPIED):
                                occupation_status=False
                                led_change(occupation_status)
                                #send changes
                                print ("Measured Distance = %.1f cm" % a)
                                print (occupation_status)
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
