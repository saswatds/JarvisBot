# Alexa Personal Assitant for Raspberry Pi
# Coded by Simon Beal and Matthew Timmons-Brown for "The Raspberry Pi Guy" YouTube channel
# Built upon the work of Sam Machin, (c)2016
# Feel free to look through the code, try to understand it & modify as you wish!
# The installer MUST be run before this code.

# !/usr/bin/python
import sys
import time
import os
import alsaaudio
import wave
import numpy
import signal
import collections
import snowboydetect

import helper  # Import the web functions of Alexa, held in a separate program in this directory

print "Welcome to Alexa. I will help you in anyway I can.\n  Press Ctrl-C to quit"

# Initialise audio buffer
audio = ""
inp = None
threshold = 0
delay_time = 0
interrupted = False
detector = None
ring_buffer = None

TOP_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_FILE = os.path.join(TOP_DIR, "resources/jarvis.pmdl")
RESOURCE_FILE = os.path.join(TOP_DIR, "resources/common.res")
DETECT_DING = os.path.join(TOP_DIR, "resources/ding.wav")
DETECT_DONG = os.path.join(TOP_DIR, "resources/dong.wav")


# Setup a ring buffer to store hotwords data
class RingBuffer(object):
    """Ring buffer to hold audio from PortAudio"""

    def __init__(self, size=4096):
        self._buf = collections.deque(maxlen=size)

    def extend(self, data):
        """Adds data to the end of buffer"""
        self._buf.extend(data)

    def get(self):
        """Retrieves data from the beginning of buffer and clears it"""
        tmp = bytes(bytearray(self._buf))
        self._buf.clear()
        return tmp


# When button is released, audio recording finishes and sent to Amazon's Alexa service
def stop_recording():
    global audio
    w = wave.open(path + 'recording.wav', 'w')  # This and following lines saves voice to .wav file
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(16000)
    w.writeframes(audio)
    w.close()
    os.system('aplay -q {}'.format(DETECT_DONG))
    if helper.cognize:
        helper.cognize()  # Call upon alexa_helper program (in this directory)
    else:
        print "Cognize has not been set, call helper.init()"
    audio = ""  # Reset the audio channel


# Whilst button is being pressed, continue recording and set "loudness"
def record():
    global audio, inp, threshold, delay_time
    l, data = inp.read()
    if l > 0:
        audio += data
        a = numpy.fromstring(data, dtype='int16')  # Converts audio data to a list of integers
        loudness = int(numpy.abs(a).mean())  # Loudness is mean of amplitude of sound wave - average "loudness"
        # if loudness is near the silence threshold then exit
        if (loudness < int(threshold * 1.1) and time.time() > delay_time):
            print "Analyzing..."
            return stop_recording()
    record()  # Recursively call record to keep recording


def set_threshold():
    global inp, threshold
    print("Setting Silence threshold")
    t_end = time.time() + 5
    while time.time() < t_end:
        l, data = inp.read()
        if l > 0:
            a = numpy.fromstring(data, dtype='int16')  # Converts audio data to a list of integers
            loudness = int(numpy.abs(a).mean())
            threshold = ((0.6 * threshold) + (0.4 * loudness))  # Implementing a complementary filter to get an average
    threshold = int(threshold)
    print("Threshold: ", threshold)


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


def setup_snowboy(decoder_model=MODEL_FILE,
                  resource=RESOURCE_FILE,
                  sensitivity=[],
                  audio_gain=1):
    global detector, ring_buffer

    tm = type(decoder_model)
    ts = type(sensitivity)
    if tm is not list:
        decoder_model = [decoder_model]
    if ts is not list:
        sensitivity = [sensitivity]
    model_str = ",".join(decoder_model)

    detector = snowboydetect.SnowboyDetect(
        resource_filename=resource.encode(), model_str=model_str.encode())
    detector.SetAudioGain(audio_gain)
    num_hotwords = detector.NumHotwords()

    if len(decoder_model) > 1 and len(sensitivity) == 1:
        sensitivity = sensitivity * num_hotwords
    if len(sensitivity) != 0:
        assert num_hotwords == len(sensitivity), \
            "number of hotwords in decoder_model (%d) and sensitivity " \
            "(%d) does not match" % (num_hotwords, len(sensitivity))
    sensitivity_str = ",".join([str(t) for t in sensitivity])
    if len(sensitivity) != 0:
        detector.SetSensitivity(sensitivity_str.encode())

    ring_buffer = RingBuffer(detector.NumChannels() * detector.SampleRate() * 5)


def setup_microphone():
    global inp
    try:
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, helper.mic_device)
    except alsaaudio.ALSAAudioError:
        print('Audio device not found - is your microphone connected? Please rerun program')
        sys.exit()
    inp.setchannels(detector.NumChannels())
    inp.setrate(detector.SampleRate())
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(1024)
    print "Channels : ", detector.NumChannels()
    print "Sample Rate: ", detector.SampleRate()


def start_detect(sleep_time):
    global inp, ring_buffer, detector, delay_time
    last_time = time.time()
    while True:
        if interrupt_callback():
            break
        # Irrespective of what the sleep is data has to be fed to the Circular Queue
        l, data = inp.read()
        if l > 0:
            ring_buffer.extend(data)

        # implement a sleep_time logic
        if (time.time() - last_time < sleep_time):
            continue
        last_time = time.time()
        data = ring_buffer.get()
        if len(data) == 0:
            continue

        ans = detector.RunDetection(data)
        if ans == -1:
            print("Error initializing streams or reading audio data")
        elif ans > 0:
            message = "Keyword " + str(ans) + " detected at time: "
            message += time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(time.time()))
            print message
            delay_time = time.time() + 3  # give at-least a 3 second delay
            os.system('aplay -q {}'.format(DETECT_DING))
            record()


if __name__ == "__main__":  # Run when program is called (won't run if you decide to import this program)
    while helper.internet_on() == False:
        print "."
    helper.init(enable_alexa=False)
    path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))
    # before doing anything else, just caliberate the threshold
    setup_snowboy(sensitivity=0.4)
    setup_microphone()
    set_threshold()
    os.system('mpg123 -q {}hello.mp3'.format(path, path))  # Say hello!
    print('Listening... Press Ctrl+C to exit')
    start_detect(sleep_time=0.03)
    print "\nYou have exited Alexa. I hope that I was useful. To talk to me again just type: python main.py"
