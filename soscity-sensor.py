import RPi.GPIO as GPIO
import os
import time
import requests
from pymongo import MongoClient

URL = os.environ['SOSCITY_URL']
SENSORID = os.environ['SOSCITY_SENSOR_ID']
TRIG = 14
ECHO = 15

mongo = MongoClient('localhost', 27017)
db = mongo.soscity

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def saveLog(error):
    db.log.insert({'sensor': SENSORID, 'message': str(error)})
    print error
    
def sendMeasurement(distance):
    print 'Distance:', distance,'cm'
    
    try:
        requests.post(URL + '/sensor/measurement', data={'sensorID': SENSORID, 'distance': distance})
    except requests.exceptions.RequestException as error:
        saveLog(error)

while True:
    GPIO.output(TRIG, False)
    print 'Waiting For Sensor To Settle'
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2) - 0.5

    if distance > 20 and distance < 400:
        sendMeasurement(distance)
    else:
        sendMeasurement(0)