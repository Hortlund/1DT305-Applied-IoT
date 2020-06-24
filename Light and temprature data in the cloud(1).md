# Light and temprature data in the cloud 
## Andreas Hortlund | ah225ba

## Project Overview
The project is made up so that you can measure light and temprature and send it to a server to then present the data visually.

The idea is to then be able to connect this further to maybe an airconditioner and electronicaldrapes, tho this is not covered in here due to resource shortage.

## Time estimate for project
If you follow the guide the project will take about 2-4 hours depending on how familiar you are with the components.

## Objective of project
The objective for this project was to learn the basics of IoT and get a better understanding of what it takes to develop for IoT-devices

## Materials needed


|           Device            |                              Purpose                               | Price |                 Link                 |
|:---------------------------:|:------------------------------------------------------------------:|:-----:|:------------------------------------:|
|            Lopy4            |                    This is the brain of it all                     | $499  |                                      |
|     Expansion board 3.1     | Lets us add more connections and connect the lopy 4 to a computer. |       | ![](https://i.imgur.com/NJsiqoQ.png) |
| Usb -A Male to Usb -b micro |                                                                    |       |                                      |
|           1 x LDR           |                                                                    |       |                                      |
|    1 x 10K ohm resistor     |                                                                    |       |                                      |
|        1 x tmp 36gz         |                                                                    |       |                                      |
|          Jumpwires          |                                Text                                | Text  |                                      |


## Putting everything togeheter
Below and exempel can be seen how to connect the circuit, becuase of the limitations of the circuit drawings program used, it doesnt look exaclty the same as mine, but will function exaclty the same, just swap out the arduino to and `Lopy4` and the pink and brown cable to anyone of the analog pin on the exapnsionboard 3.1
![](https://i.imgur.com/XG5AyTJ.png)


## Gude to set up docker https://www.home-assistant.io/blog/2017/04/25/influxdb-grafana-docker/

## draw circuit 

choose wifi becuase of lora connectivity where i live 

send data to influx 
https://www.influxdata.com/blog/getting-started-python-influxdb/

## The code 

#### boot.py
https://docs.pycom.io/tutorials/all/wlan
```
#imports machine modules
import machine 
#import wlan from network module
from network import WLAN

#sets the wlan mode to a station
wlan = WLAN(mode=WLAN.STA)
#scans for available network
nets = wlan.scan()
#for each net check if SSID checksout with the one given
for net in nets:
    if net.ssid == 'SSID':
        print('Network found!')
        #connect with the wpa key
        wlan.connect(net.ssid, auth=(net.sec, 'WPA-2 KEY'), timeout=5000)
        while not wlan.isconnected(): # otherwise idle if net is not found
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!') # notify connection success
        break
```

#### main.py

```
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
```

#### urequests.py
https://github.com/micropython/micropython-lib/tree/master/urequests



## Platform
Local instance of docker running telegraf, influxDB and Grafana to get, store and present the data that the sensors send. 

If you dont have docker then go ahead and download it from here: https://www.docker.com/get-started

Below image was used.
https://github.com/samuelebistoletti/docker-statsd-influxdb-grafana

Run below command to pull the latest image the run the next command to download and install
```
# docker pull samuelebistoletti/docker-statsd-influxdb-grafana
# docker run --ulimit nofile=66000:66000 \
  -d \
  --name docker-statsd-influxdb-grafana \
  -p 3003:3003 \
  -p 3004:8888 \
  -p 8086:8086 \
  -p 8125:8125/udp \
  samuelebistoletti/docker-statsd-influxdb-grafana:latest
```

Since database cant be changed in the webUI due to everythig being built by configfiles, if you want to change the default datastore follow below instructions.

Change the uppercase letters below to your database credentials. Open the file with `nano` to edit.
```
# cd /etc/grafana/provisioning/datasources
# cat influxDB.yml
datasources:
  - name: InfluxDB
    type: influxdb
    access: proxy
    database: DATABASE
    user: USER
    password: PASS
    url: http://localhost:8086
    isDefault: true
```
