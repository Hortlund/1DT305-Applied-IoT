#Import all pycom and micropython modules needed 
import pycom
import machine
import _thread
import time
import ujson as json

#This import the urequests folder as requests with the urequests.py file inside
#This is needed because of the way the filesystem is structured on the pycom device
import urequests as requests


adc = machine.ADC() # creates a analog to digital conversion object
apin = adc.channel(pin='P16') # maps pin p16 to apin variable
bpin = adc.channel(pin='P15') # maps pin p15 to bpin variable

url = 'URL' #url for upload to database


while(1): # infinite loop
    temprature = (bpin.voltage() - 500) / 10 # calculation to get temprature from tmp 36gz thermistor
    lux = (250/(0.004*apin.voltage())-50) # rough calculation to get lux value from ldr, give a somewhat correct response
    print("Temprature: {:.1f}".format(temprature)) #prints temp
    print("Lux: {:.1f}".format(lux)) #prints lux
    #structures the payload so that influxdb can direclty receive it, with temp and lyx as part of the body
    payload = "sensors,value=\"Temp\" temprature={:.1f}\nsensors,value=\"Light\" lux={:.1f}".format(temprature,lux)
    requests.post(url,data=payload) # sends the data using urequests.py function
    print("data sent...")
    time.sleep(10) # waits 10 sec before doing it again

