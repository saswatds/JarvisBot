import requests
import cognitive

mic_device = "plughw:1"

cognize = None


# Check whether your Raspberry Pi is connected to the internet
def internet_on():
    print "Checking Internet Connection"
    try:
        r = requests.get('http://iamawesome.com')
        print "All systems GO"
        return True
    except:
        print "Connection Failed"
        return False


def init():
    global cognize
    cognize = cognitive.doit
