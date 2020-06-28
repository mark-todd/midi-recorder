def call():
    print(1)


def event(channel, my_callback_func, bounce_ms):
    GPIO.add_event_detect(channel, GPIO.RISING, callback=call(), bouncetime=200)

from shutil import copyfile
import os
import signal
import subprocess
import music21
import RPi.GPIO as GPIO
import time
from mido import MidiFile

#Define pin numbers
Record_pin=7
PlayPause_pin=11
LoopPlay_pin=13
IncSpeed_pin=15
DecSpeed_pin=19
ResSpeed_pin=21
Shutdown_pin=24
Led_pin=26
print(os.getcwd())

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Record_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PlayPause_pin, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LoopPlay_pin, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IncSpeed_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DecSpeed_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ResSpeed_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Led_pin, GPIO.OUT)
GPIO.output(Led_pin,1)

#Define pin numbers
Record_pin=7
PlayPause_pin=11
LoopPlay_pin=13
IncSpeed_pin=15
DecSpeed_pin=19
ResSpeed_pin=21
Shutdown_pin=24
Led_pin=26
print(os.getcwd())

event(7,1,100)