# Artifical Intelligence Pi
### Turn your Raspberry Pi into your own personal assistant using the Amazon Echo Alexa voice service!

This repository accompanies my tutorial. This is a complete guide on setting up Alexa for your Raspberry Pi. I have adapated the code to use the fantastic Raspberry Pi SenseHAT for input and also RGB graphics! You can watch the full tutorial here: https://www.youtube.com/watch?v=tcI8ibjUOzg

Here is an example of one of the things you can ask your new Raspberry Pi personal assistant: 

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Just spent a lot of time hacking my <a href="https://twitter.com/Raspberry_Pi">@Raspberry_Pi</a> and SenseHAT to turn it into my own personal assistant! <a href="https://twitter.com/HAL9000_">@HAL9000_</a> <a href="https://t.co/2jO4PEqW8Y">pic.twitter.com/2jO4PEqW8Y</a></p>&mdash; The Raspberry Pi Guy (@RaspberryPiGuy1) <a href="https://twitter.com/RaspberryPiGuy1/status/737364956354596864">May 30, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

##Information
You will need:
* A Raspberry Pi connected to the internet (my tutorial uses the Raspberry Pi 3, but it should work with every model compatible with the Raspberry Pi SenseHAT - B+,A+,Pi 2,Pi 3,Pi Zero)
* An SD Card with a fresh install of Raspbian (tested with 2016-05 Raspbian)
* An External Speaker with 3.5mm Jack (like this one: https://www.amazon.co.uk/XMI-Generation-Capsule-Compatible-Smartphones/dp/B001UEBN42/ref=sr_1_3?ie=UTF8&qid=1464643924&sr=8-3&keywords=mini+speaker)
* A USB Microphone (ideally make sure it is a plug n play one! I used this inexpensive one in the video: https://www.amazon.co.uk/Tonor-Professional-Condenser-Microphone-Computer/dp/B01142EPO4/ref=sr_1_3?ie=UTF8&qid=1464644011&sr=8-3&keywords=usb+microphone)
* A Raspberry Pi Official SenseHAT add-on (https://thepihut.com/products/raspberry-pi-sense-hat-astro-pi)

### Installation

For all instructions and processes, see my tutorial. Included below are the commands needed to type in to the console:

Display your Raspberry Pi's IP address: ifconfig

Download the code: git clone https://github.com/the-raspberry-pi-guy/Artificial-Intelligence-Pi

Change into the new directory: cd Artificial-Intelligence-Pi

Run the setup script: sudo ./setup.sh

Run Alexa: python main.py

### FAQ & Troubleshooting

This section will be added to as people report their troubles and ask questions.

- 'x,y,z' didn't work and an error was generated! What do I do?
9/10 times this kind of error is down to accidental mistakes. As I try to stress in the video, check and check again that the commands and information you enter in the process are correct. If you come across a nasty error, just try again - it normally fixes things.

- Can Alexa speak 'x' language?
To the best of my knowledge, Alexa is only available in English (US) at the moment. Amazon has over 1000 employees working on Alexa however - so this may change in the future.

- Can this be used to control 'x' on a Raspberry Pi?
As of current, Alexa cannot be customised to control things directly on your Raspberry Pi, such as turn GPIO pins on and off. The Alexa Voice Service does all of its processing in the cloud - none of it happens locally on the Pi. If you would like to learn a little bit more about what AVS can do, read this article: http://fieldguide.gizmodo.com/everything-you-can-say-to-your-amazon-echo-1762166130

- Do I have to use a SenseHAT to use Alexa?
The answer to this question is no, you do not need a SenseHAT to use Alexa. You do however need a SenseHAT to follow my tutorial. This is because I have edited the program to work with SenseHAT. I did this because, in my opinion, the SenseHAT is a fantastic add-on that makes the task of activating Alexa much more simple. If you take a look at the GitHub repo that I forked from, the code there triggers Alexa by using a button attached to the GPIO pins. As per Amazon's T&Cs you can NOT activate the service using your voice.

- Can I use earphones/headphones instead of a speaker?
Yes. Any 3.5mm audio device should work and that includes headphones/earphones.

- I have a different microphone to the one that you used in the tutorial, how can I ensure that it works?
There is no easy answer to this question - you will just have to try it! As I said in the tutorial, plug 'n' play microphones are ideal for this as you don't have to fiddle around with drivers.

- Alexa thinks that I live in Seattle! How do I change that?
Amazon Echo is an American product and consequently Alexa will most likely think you are in Seattle. Whilst I have not tried it, I believe there is a companion app that allows you to change the location of your device. This may not be available in every country however. Alternatively, end your commands with your location. For example: "What is the weather like in Cambridge, UK?"

### Thank You!

The work in this repository is based off of the work of Novaspirit and Sammachin. I would also like to thank my good friend Simon Beal (muddyfish) for his help in getting this up and going!

Thanks for watching,

Matthew Timmons-Brown

The Raspberry Pi Guy

www.youtube.com/theraspberrypiguy

www.theraspberrypiguy.com

@RaspberryPi1
