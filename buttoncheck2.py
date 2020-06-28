buttons=[7,11,13,15,19,21,24,8,10,12,16,18,22]
LED=26

i=0
import GPIO2 as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD())

while i<len(buttons):
    GPIO.setup(buttons[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    i=i+1

GPIO.setup(LED, GPIO.OUT)

while True:
    j=0
    array=[]
    while j<len(buttons):
        array.append(GPIO.input(buttons[j]))
        j=j+1
    print(array)
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(LED, GPIO.LOW)