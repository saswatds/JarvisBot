# Alexa Personal Assitant for Raspberry Pi
# Coded by Simon Beal and Matthew Timmons-Brown for "The Raspberry Pi Guy" YouTube channel
# Built upon the work of Sam Machin, (c)2016
# Feel free to look through the code, try to understand it & modify as you wish!
# The installer MUST be run before this code.

#!/usr/bin/python
import sys
import time
import os
import alsaaudio
import wave
import numpy
import copy

import alexa_helper # Import the web functions of Alexa, held in a separate program in this directory

print "Welcome to Alexa. I will help you in anyway I can.\n  Press Ctrl-C to quit"

# Initialise audio buffer
audio = ""
inp = None
threshold = 0


# When button is released, audio recording finishes and sent to Amazon's Alexa service
def stop_recording():
    global audio
    w = wave.open(path+'recording.wav', 'w') # This and following lines saves voice to .wav file
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(16000)
    w.writeframes(audio)
    w.close()
    alexa_helper.alexa() # Call upon alexa_helper program (in this directory)
    audio = "" # Reset the audio channel

# Whilst button is being pressed, continue recording and set "loudness"
def record():
    global audio, inp, threshold
    l, data = inp.read()
    if l > 0:
        audio += data
        a = numpy.fromstring(data, dtype='int16') # Converts audio data to a list of integers
	loudness = int(numpy.abs(a).mean()) # Loudness is mean of amplitude of sound wave - average "loudness"
        # if loudness is near the silence threshold then exit
        if(loudness < threshold*1.1):
            print "Analyzing..."
            return stop_recording()
    record() # Recursively call record to keep recording

def set_threshold():
    global inp, threshold
    print("Setting Silence threshold") 
    t_end = time.time() + 5
    while time.time() < t_end:
        l, data = inp.read()
        if l > 0:
            a = numpy.fromstring(data, dtype='int16') # Converts audio data to a list of integers
            loudness = int(numpy.abs(a).mean())
            threshold = ((0.6*threshold) + (0.4*loudness)) #Implementing a complementary filter to get an average
    threshold = int(threshold)
    print("Threshold: ", threshold)

def setup_microphone():
    global inp
    try:
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, alexa_helper.device)
    except alsaaudio.ALSAAudioError:
        print('Audio device not found - is your microphone connected? Please rerun program')
        sys.exit()
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(1024)

# Continually loops for events, if event detected and is the middle joystick button, call upon event handler above
def event_loop():
    try:
        while True:
            cmd = raw_input('Enter R to start recording.... Ctrl-C to exit: ')
            record()
    except KeyboardInterrupt: # If Ctrl+C pressed, pass back to main body - which then finishes and alerts the user the program has ended
        pass

if __name__ == "__main__": # Run when program is called (won't run if you decide to import this program)
    while alexa_helper.internet_on() == False:
        print "."
    token = alexa_helper.gettoken()
    path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))
    # before doing anything else, just caliberate the threshold
    os.system('mpg123 -q {}hello.mp3'.format(path, path)) # Say hello!
    setup_microphone()
    set_threshold() 
    event_loop()
    print "\nYou have exited Alexa. I hope that I was useful. To talk to me again just type: python main.py"
