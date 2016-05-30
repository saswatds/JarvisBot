#!/usr/bin/python
import sys
import time
from sense_hat import SenseHat
import RPi.GPIO as GPIO
import os
import alsaaudio
import wave
from evdev import InputDevice, list_devices, ecodes

import alexa_helper

print("Press Ctrl-C to quit")
time.sleep(1)

sense = SenseHat()
sense.clear()  # Blank the LED matrix

found = False;
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        found = True;
        break

if not(found):
    print('Raspberry Pi Sense HAT Joystick not found. Aborting ...')
    sys.exit()

audio = ""
inp = None

def release_button():
    global audio, inp
    w = wave.open(path+'recording.wav', 'w') 
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(16000)
    w.writeframes(audio)
    w.close()
    print("Finished saving", len(audio))
    alexa_helper.alexa()
    inp = None
    audio = ""

def press_button():
    global audio, inp
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, alexa_helper.device)
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(1024)
    audio = ""
    l, data = inp.read()
    if l:
        audio += data

def continue_pressed():
    global audio, inp
    l, data = inp.read()
    if l:
        audio += data
#        print(l)

def handle_enter(pressed):
    handlers = [release_button, press_button, continue_pressed]
    handlers[pressed]()

def event_loop():
    try:
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_ENTER:
                handle_enter(event.value)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    while alexa_helper.internet_on() == False:
        print "."
    token = alexa_helper.gettoken()
    path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))
    os.system('mpg123 -q {}1sec.mp3 {}hello.mp3'.format(path, path))
    event_loop()
