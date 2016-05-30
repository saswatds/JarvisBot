#!/usr/bin/python
import sys
import time
from sense_hat import SenseHat
import RPi.GPIO as GPIO
import os
import alsaaudio
import wave
import numpy #May not be in default build
import copy
from evdev import InputDevice, list_devices, ecodes #May not be in default build

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

#We're British and we spell Colour correctly :)
colours = [[255, 0, 0], [255, 0, 0], [255, 105, 0], [255, 223, 0], [170, 255, 0], [52, 255, 0], [0, 255, 66], [0, 255, 183]]

max_bright = 1024

def set_display(brightness):
    mini = [[0,0,0]]*8
    brightness = max(1,min(brightness, max_bright)/(max_bright/8))
    mini[8-brightness:] = colours[8-brightness:]
#    print mini
    display = sum([[col]*8 for col in mini], [])
    sense.set_pixels(display)
#    print len(new)

def release_button():
    global audio, inp
    sense.set_pixels([[0,0,0]]*64)
    w = wave.open(path+'recording.wav', 'w') 
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(16000)
    w.writeframes(audio)
    w.close()
    sense.show_letter("?")
    print "Finished saving"
    alexa_helper.alexa(sense)
    sense.clear()
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
        a = numpy.fromstring(data, dtype='int16')
        loudness = int(numpy.abs(a).mean())
        set_display(loudness)

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
    os.system('mpg123 -q {}hello.mp3'.format(path, path))
    event_loop()
