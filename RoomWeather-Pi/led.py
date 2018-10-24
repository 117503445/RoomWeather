import RPi.GPIO as gpio
import time
#led=0,1,2,else Green,Yellow,Red,Null
def light(led):
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    ports=[15,13,11]
    for i in range(3):
        gpio.setup(ports[i],gpio.OUT)
        if i==led:
            gpio.output(ports[i],gpio.HIGH)
        else:
            gpio.output(ports[i],gpio.LOW)