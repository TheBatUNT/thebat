#!/usr/bin/python
from espeak import espeak
import MySQLdb
import serial
import time
import os.path

#if os.path.exists("dev/rfcomm0"):
ser = serial.Serial('/dev/rfcomm1',9600)
#else:
#	print 'Could not connect to navigation bluetooth'
#	exit()
#if os.path.exists("dev/rfcomm1"):
 #       ser1 = serial.Serial('/dev/rfcomm1',9600)
#else:
 #       print 'Could not connect to object  bluetooth'
  #      exit()


espeak.synth("Turning on Device")
ser.flushInput()
time.sleep(2)
flag1 = 1 #flag for 20-10 ft
flag2 = 1 #flag for 15-10 ft
flag3 = 1 #flag for 10-5 ft
flag4 = 1 #flag for 5-0 ft
flag5 = 1 #flag for wall

flag6 = 1 #Precedence flag for SF sensor
flag7 = 1 #Precedence flag for SB sensor


def detect(sensorData): #Say whether it is wall or object
    time.sleep(2)
    if sensorData == "SF":
        espeak.synth("Wall in")
        time.sleep(1)
#	flag6 = 0 #flag triggered
    elif sensorData == "SB":
        espeak.synth("Object in")
        time.sleep(2)
#	flag7 =0 #flag triggered

    elif sensorData == "SL":
          espeak.synth("opening on the left")
    elif sensorData == "SR":
          espeak.synth("Opening on the right") 
  #  elif sensorData == "C":
   #     espeak.synth("Device Calibrating, Please Wait")
    return;
def userLoc(sensorData):
    lat = float(serialdata.split(" ")[1]) #current Latitude
    lon = float(serialdata.split(" ")[2]) #current Longitude
    print lat, lon
    db = MySQLdb.connect("localhost","root","hearmeout","thebat")
    query = "UPDATE currentUser SET Latitude=%f, Longitude=%f"%(lat,lon)
    cursor = db.cursor()
    try:
        cursor.execute(query)
        db.commit()
        print "Success"
    except:
        db.rollback()
        print "Failure"
    db.close()
    return;
while 1: 
    serialdata = ser.readline() # storing serial data
    sensor = serialdata.split(" ")[0]
    if sensor == "UP":
        userLoc(serialdata)
    elif sensor == "LC":
        print serialdata
    else:
        distance = serialdata.split(" ")[1]
        distance = float(distance) #make distance a float
        distance = distance/12  #converting inches to feet
        distance = round(distance,0) #rounding to 0 dec place
        distance = int(distance) #Removing ".0" from output
        distance1 = str(distance) #make distance a string for tts
        print serialdata #Print Sensor and Distance Data from Arduino
        if distance < 20 and distance > 15 and flag1 == 1  : #between 20-10ft
            detect(sensor)
            espeak.synth(distance1)
            espeak.synth("feet")
            time.sleep(1)
            flag1 = 0 #Set current flag to 0 and rest all others to 1
            flag2 = 1
            flag3 = 1
            flag4 = 1
        if distance < 15 and distance > 10 and flag2 == 1  : #between 15-10ft
            detect(sensor)
            espeak.synth(distance1)
            espeak.synth("feet")
            time.sleep(2)
            flag2 = 0
            flag1 = 1
            flag3 = 1
            flag4 = 1
        if distance < 10 and distance > 5 and flag3 == 1: #between 10-5ft
            detect(sensor)
            espeak.synth(distance1)
            espeak.synth("feet")
            time.sleep(2)
            flag3 = 0
            flag1 = 1
            flag2 = 1
            flag4 = 1
        if distance < 5 and distance > 0 and flag4 ==1 : #between 5-0ft
            detect(sensor)
            espeak.synth(distance1)
            espeak.synth("feet")
            time.sleep(2)
            flag4 = 0
            flag3 = 1
            flag2 = 1
            flag1 = 1
        if distance == 0:
            detect(sensor)
            flag1 = 1
            flag2 = 1
            flag3 = 1
            flag4 = 1
