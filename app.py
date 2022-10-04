from flask import Flask, render_template
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
        if measurements != 'time' and stats[measurements]['valueList'] != []:

                for stats[measurements]['minValue'] in measurements:
                    minValue = min(stats[measurements]['valueList'])
                    stats[measurements]['minValue'] = minValue 

                for stats[measurements]['maxValue'] in measurements:
                    maxValue = max(stats[measurements]['valueList'])
                    stats[measurements]['maxValue'] = maxValue
    
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
    global stats, humidity, temperature, brightness, measuredData

    # Initialize variables
    measuredData = [humidity, temperature, brightness]
    value = 0
    
    if humidity != 0 and temperature != 0: # exception for first Arduino launch
        for i, measurements in enumerate(stats): # iterate over every measurement key in stats dict
            if measurements != 'time': # exception for time key

                # Store measurement to respective key dictionary
                value = measuredData[i]
                stats[measurements]['currentValue'] = int(value)
                stats[measurements]['valueList'].append(value)

        currentTime = get_time()
        stats['time'] = currentTime

    print(stats)

def measureLDR(data): # Store measurement for brightness
    global brightness, measuredData
    brightness = data[2]
    
def measure(data): # Store measurement for temp and hum
    global humidity, temperature, measuredData
    if data[3] == 0: 
        humidity = data[4]
        temperature = data[5]

def setup(): # Initialize sensors
    global board, stats
    board = CustomPymata4(com_port="COM3")
    board.set_pin_mode_dht(DHTPIN, sensor_type = 11, differential = .05, callback = measure)
    board.set_pin_mode_analog_input(LDRPIN, callback = measureLDR, differential = 10)
    board.

def getData():
    global stats

    store_values()
    get_min_max()
    avg_measure()
    board.displayShow(stats['humidity']['currentValue'])
    time.sleep(0.01)

    return stats

setup()
 

@app.route('/')
def dashboard():
    getData()
         
    return render_template('index.html', stats = stats)
