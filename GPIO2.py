def setwarnings(Warn):
    if Warn:
        print('warnings on')
    else:
        print('warnings off')

def BOARD():
    print('Board numbering set')

def IN():
    do='nothing'

def OUT():
    do='nothing'
def setup(number, Modehere, pull_up_down=''):
    print('Pin no '+str(number)+' set to in')

def setmode(Modehere):
    print('Mode set')

def input(number):
    while True:
        try:
            filehere=open('pinstate.txt','r+')
            linex=filehere.readline()
            inspect=int(linex[number])
            break
        except:
            continue
    if inspect==1:
        return True
    else:
        return False
def PUD_DOWN():
    print('Puds down')
import time
