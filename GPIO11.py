def Kill(pro):
    try:
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    except:
        pass

def Run(command):
    pro = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    return pro

def KillandRun(command,pro):
    try:
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    except:
        pass
    finally:
        pro = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
    return pro

def Loop(command):
    pro = subprocess.Popen('while true; do '+command+'; done', stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    return pro

def CheckPro(pro):
    try:
        poll=pro.poll()
        if poll==None:
            #Still Running
            return True
        else:
            return False
    except:
        do='nothing'


def Start_Record(outputfile):
    recid=Run('arecordmidi -p 20:0 '+str(outputfile))
    return recid


def Play(inputfile):
    playid=Run('aplaymidi -p 20:0 '+str(inputfile))
    return playid

def LoopPlay(inputfile):
    playid=Run('aplaymidi -p 20:0 '+str(inputfile))
    return playid

def Shutdown():
    os.system('sudo shutdown -h now')
    

def Speed(inputfile,outputfile,factor):
    newscore = inputfile.scaleOffsets(factor).scaleDurations(factor)
    newscore.write('midi',outputfile)

def Length(inputfile):
    mid=MidiFile(inputfile)
    return mid.length

def trap(pinnum):
    while True:
        time.sleep(0.1)
        if GPIO.input(pinnum)==1:
            continue
        else:
            break


from shutil import copyfile
import os
import signal
import subprocess
import music21
import RPi.GPIO as GPIO
import time
from mido import MidiFile

#Set song id
songid=''
#Define pin numbers
Record_pin=7
PlayPause_pin=11
LoopPlay_pin=13
IncSpeed_pin=15
DecSpeed_pin=19
ResSpeed_pin=21
Shutdown_pin=24
Led_pin=26

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
#set State values
playing=0
recording=0
looping=0
Factor=1
playid=0

RecordingOut='output.mid'
InFile='output.mid'
#Prepare score for rescale
score = ''
loop_tweak=-0.17
print('loaded')
GPIO.output(Led_pin,1)
while True:
    time.sleep(0.1)
    #Check possibilities for record press
    if GPIO.input(Record_pin)==1:
        #If not recording - start
        if recording==0:
            print('start')
            recid=Start_Record(RecordingOut)
            recording=1
            #Trap it here till release
            trap(Record_pin)
        #If it is recording - stop
        elif recording==1:
            print('stop')
            Kill(recid)
            score = music21.converter.parse(RecordingOut)
            recording=0
            #Trap it here till release
            trap(Record_pin)
    #Possibles for play press
    elif GPIO.input(PlayPause_pin)==1:
        #if not playing - start
        if playing==0 and recording==0 and looping==0:
            playid=Play(InFile)
            playing=1
            #Trap it here till release
            trap(PlayPause_pin)
        #if it is playing stop
        elif playing==1:
            Kill(playid)
            playing=0
            #Trap it here till release
            trap(PlayPause_pin)
    elif GPIO.input(IncSpeed_pin)==1:
        if playing==0 and recording==0 and looping==0:
            Factor=Factor*0.9
            Speed(score,InFile,Factor)
            #Trap it here till release
            trap(IncSpeed_pin)
    elif GPIO.input(DecSpeed_pin)==1:
        if playing==0 and recording==0 and looping==0:
            Factor=Factor*1.1111
            Speed(score,InFile,Factor)
            #Trap it here till release
            trap(DecSpeed_pin)
    elif GPIO.input(ResSpeed_pin)==1:
        if playing==0 and recording==0 and looping==0:
            Factor=1
            Speed(score,InFile,Factor)
            #Trap it here till release
            trap(ResSpeed_pin)
    elif GPIO.input(LoopPlay_pin)==1:
        #if normal playing isn't happening
        if playing==0 and recording==0:
            #If it's not looping - start looping
            if looping==0:
                looping=1
                playid=LoopPlay(InFile)
                start_time=time.time()
                #Trap till release
                trap(LoopPlay_pin)
            #If it's looping - stop looping
            elif looping==1:
                looping=0
                Kill(playid)
                #Trap till release
                trap(LoopPlay_pin)
    elif GPIO.input(Shutdown_pin)==1:
        print('Shutdown()')
    #If it's looping
    elif looping==1:
        if float(Length(InFile))<float(time.time()-start_time-loop_tweak):
            playid=LoopPlay(InFile)
    #If the music has stopped - it's stopped playing
    elif not CheckPro(playid):
        playing=0
    else:
        do='nothing'
