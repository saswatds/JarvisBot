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

- More details will be added over time and as people report their troubles!

### Thank You!

The work in this repository is based off of the work of Novaspirit and Sammachin. I would also like to thank my good friend Simon Beal (muddyfish) for his help in getting this up and going!

Thanks for watching,

Matthew Timmons-Brown

The Raspberry Pi Guy

www.youtube.com/theraspberrypiguy

www.theraspberrypiguy.com

@RaspberryPi1
