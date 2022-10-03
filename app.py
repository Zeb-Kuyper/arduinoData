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

measuredData = []
valueList = []

stats = {

    'humidity':{
    'currentValue':0,
    'valueList': [],
    'averageValue':0,
    'minValue':0,
    'maxValue':0,
},
    'temperature':{
    'currentValue':0,
    'valueList': [],
    'averageValue':0,
    'minValue':0,
    'maxValue':0,
},
    'brightness':{
    'currentValue':0,
    'valueList': [],
    'averageValue':0,
    'minValue':0,
    'maxValue':0,
},

    'time':0
}

def get_min_max():
    global stats

    for measurements in stats:
        if measurements != 'time':
            if stats[measurements]['valueList'] != []:
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
        if measurements != 'time':
            if len(stats[measurements]['valueList']) != 0:
                average_value = sum(stats[measurements]['valueList'])/len(stats[measurements]['valueList'])
            else:
                average_value = 0
                
            stats[measurements]['averageValue'] = average_value

    print(stats)

def store_values():
    global stats, data, humidity, temperature, brightness, measuredData
    measuredData = [humidity, temperature, brightness]
    value = 0

    if humidity != 0 and temperature != 0:
        for i, measurements in enumerate(stats):
            if measurements != 'time':
                value = measuredData[i]
                stats[measurements]['currentValue'] = int(value)
                stats[measurements]['valueList'].append(value)

        currentTime = get_time()
        stats['time'] = currentTime

    print (stats)

def measureLDR(data):
    global brightness, measuredData
    brightness = data[2]
    measuredData = [humidity, temperature, brightness]

    
def measure(data):
    global humidity, temperature, measuredData
    
    if data[3] == 0:
        humidity = data[4]
        temperature = data[5]
    
    measuredData = [humidity, temperature, brightness]

def setup():
    global board
    board = CustomPymata4(com_port="COM3")
    board.set_pin_mode_dht(DHTPIN, sensor_type = 11, differential = .05, callback = measure)
    board.set_pin_mode_analog_input(LDRPIN, callback = measureLDR, differential = 10)

def loop():
    global stats
    quit = input('continue?:')
    store_values()
    get_min_max()
    avg_measure()
    print(stats)
    board.displayShow(stats['humidity']['currentValue'])
    time.sleep(0.01)

setup()
while True:
    try:
                loop()  
    except KeyboardInterrupt: # crtl+C
        print ('shutdown')
        board.shutdown()
        sys.exit(0)   

# @app.route('/')
# def dashboard():
#         brightness_data = stats['brightness']
