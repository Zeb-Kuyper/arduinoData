from audioop import avg
from msilib import datasizemask
from flask import Flask, current_app
import time, sys
from fhict_cb_01.CustomPymata4 import CustomPymata4

app = Flask(__name__)

# Constants

DHTPIN = 12
LDRPIN = 2

# Globals

humidity = 0
temperature = 0
brightness = 0

measuredData = [humidity, temperature, brightness]

data = {
    'currentValue':0,
    'valueList':[],
    'averageValue':0,
    'minValue':0,
    'maxValue':0,
}

stats = {
    'humidity':data,
    'temperature':data,
    'brightness':data,
    'time':0
}

def get_min_max():
    global stats

    for measurements in stats:
        if measurements is type(dict):
            for stats[measurements]['minValue'] in measurements:

                minValue = min(stats[measurements]['valueList'])
                stats[measurements]['minValue'] = minValue 

            for stats[measurements]['maxValue'] in measurements:
                
                maxValue = max(stats[measurements]['valueList'])
                stats[measurements]['maxValue'] = maxValue
    print(stats)
    
def get_time():
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)

    return currentTime
     
def avg_measure():
    global stats

    for measurements in stats:
        if stats[measurements] is type(dict):
            for stats[measurements]['averageValue'] in measurements:

                valueList = stats[measurements][data]['valueList']
                averageValue = sum(valueList)/len(valueList)
                stats[measurements][data]['averageValue'] = averageValue

    print(stats)

def store_values():
    global stats, data, humidity, temperature, brightness, measuredData

    for measurement in measuredData:
        stats[str(measuredData[measurement])][data]['currentValue'] = measurement

    stats['time'] = get_time
    print (stats)

def measureLDR(data):
    global brightness
    brightness = data[2]
    
def measure(data):
    global humidity, temperature, stats
    
    if data[3] == 0:
        humidity = data[4]
        temperature = data[5]



def setup():
    global board
    board = CustomPymata4(com_port="COM3")
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback = measure)
    board.set_pin_mode_analog_input(LDRPIN, callback=measureLDR, differential=10)
    measure()
    measureLDR()
    store_values()
    avg_measure()
    get_min_max()

setup()

# @app.route('/')
# def dashboard():
#         brightness_data = stats['brightness']
