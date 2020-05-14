
#Before Running the code Install the Lib and make sure you replace the Thingspeak and Twilio account Keys

import RPi.GPIO as GPIO
import time
import urllib.request
import threading
from twilio.rest import Client
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setwarnings(False)

def Distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.0001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
            TimeElapsed = StopTime - StartTime
            distance = (TimeElapsed * 34300)/2
    return distance


def Thingspeak():
    threading.Timer(5, Thingspeak).start()
    val = Distance()
    url = "https://api.thingspeak.com/update?api_key="  #In the place of this url put your own ThingsPeak Account URL
    key="8LSH42S9QZMFYSZN"                              #In the place of this key put your account key
    header="field2="+str(val)                           #Enter the filed you want to show data in
    nurl=url+key+header
    print(nurl)
    data = urllib.request.urlopen(nurl)
    return data


account_sid = "AC22879245ec59bca549b805da490d1352"     #In the place of this accnt_sid put your twilio account sid
auth_token = "e7b0a26f216c429e5f1d944612075356"        #In the place of this token put your twilio account token
client = Client(account_sid, auth_token)
message = client.messages \
    .create(
        body="Bin Full till " +str(Distance()),
        from_="+12018200738",                          #In the place of this number put your twilio account phone number
        to="+917045159227"                             #In the place of this number put your required reciever twilio verified number
    )
print(message.sid)

if __name__ == "__main__":
    try:
        while True:
            dist = Distance()
            print("Measured distance = %.1f cm"% dist)
            ThingsData=Thingspeak()
            print("THINGSPEAK DATA = %.1f cm"% dist)
            time.sleep(1)
    except KeyboardInterrupt:
        print("MEASURING STOPPED BY USER")
        GPIO.cleanup()