#!/usr/bin/python
from espeak import espeak
import MySQLdb
import serial
import time
import os.path
import math
from espeak import core as espeak_core

timerSeconds = 2 #Time between command repeats itself in seconds
timerProximity = 1
wallElapsed = 0  #starting value for elapsed
objectElapsed = 0
openingBothElapsed = 0
openingLeftElapsed = 0
openingRightElapsed = 0
leftProximityElapsed = 0
rightProximityElapsed = 0
ser = serial.Serial('/dev/rfcomm1',9600,timeout = 5)#wall, right and left sensor rfcomm
ser2 = serial.Serial('/dev/rfcomm0',9600,timeout =5)#object rfcomm

# Call espeak.synth() and wait for utterence to be finished.
# From https://answers.launchpad.net/python-espeak/+question/244655
def say(*args):
  done_synth = [False]
  def synth_callback(event, pos, length):
    if event == espeak_core.event_MSG_TERMINATED:
      done_synth[0] = True
  espeak.set_SynthCallback(synth_callback)
  call_result = espeak.synth(*args)
  while call_result and not done_synth[0]:
    time.sleep(0.05)
  return call_result


say("Turning on Device")
time.sleep(2)
say("The Bat")
time.sleep(1)
say("Indoor navigation and obstacle detection")

# Openning DB connection 
# Get user measurement settings
def convchk():
    db = MySQLdb.connect("localhost","root","hearmeout","thebat")
# Preparing cursor object using cursor() method

    cursor = db.cursor()
    sql = "SELECT * FROM currentUser"

    try:
         #Execute SQL commands
            cursor.execute(sql)
            results = cursor.fetchall()
            flagMeas = results[0][3]

    except:
        print "Error: Unable to fetch measurement"
    db.close
    del results
    return flagMeas

flagMeas=convchk()


#############NAVIGATION FUNCTION###########################
# Store users current location in DB
def userLoc(sensorData):
    print sensorData
    lat = float(sensorData.split(" ")[7]) #current Latitude
    lon = float(sensorData.split(" ")[8]) #current Longitude
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
###########################################################

###############INCHES to FEET function###################
def conv(feetDistance):
    feetDistance = float(feetDistance) #make distance a float
    feetDistance = feetDistance/12  #converting inches to feet
    feetDistance = round(feetDistance,0) #rounding to 0 dec place
    feetDistance = int(feetDistance) #Removing ".0" from output
    return feetDistance;
#####################################################

###############Inches to Meters##################
def conv2meter(meterDistance):
    meterDistance = float(meterDistance) #make distance a float
    meterDistance = meterDistance/39.37 #converting to meter
    meterDistance= round(meterDistance,1) #rounding to 0 dec place
    print meterDistance
    return meterDistance;
##############################################

#############Calling meters or feet#######
def callmeas(flagMeas,distanceforconv2):
    if flagMeas == 1 : #meters
	distance5= conv2meter(distanceforconv2)
        return distance5;
    elif flagMeas == 0 : #feet
    	 distance6 = conv(distanceforconv2)
         return distance6;
def flagmeascheck(flagMeas):
    if flagMeas == 1 :
	say("Meters")
    elif flagMeas == 0 :
	say("Feet")
    return;




c1=0 #counter for timeout for headphone bluetooth
c2=0 #counter for timeout for belt bluetooth 
while 1: 
    flagMeas=convchk() 
    try:
        serialdata = ser.readline() # storing serial data
    except:
        say("Headphone Bluetooth is disconnected")
        print "headphone Bluetooth is disconnected"
        time.sleep(5)
        c1=c1+1
        if c1==5:
            print "Time out on headphone bluetooth, device shutting down"
            say("Device is shutting down check Headphone bluetooth and try again")
#            os.system("sudo shutdown -h now") 
            exit()
        continue
    try:
        serialdata2 = ser2.readline() #storing serial data 2
    except:
        say("Belt Sensor is disconnected")
        print "Belt sensor is disconnected"
        time.sleep(5)
        c2=c2+1
        if c2==5:
            print "Time out on Belt bluetooth, device shutting down"
            say("Device is shutting down check Belt bluetooth and try again")
#            os.system("sudo shutdown -h now") 
            exit()
        continue
    tempabc = serialdata.split(" ") #length of serialdata 
    tempabcd = serialdata2.split(" ")
    stringlenSerial2 = len(tempabcd)
    stringlenSerial = len(tempabc) #setting to
    if stringlenSerial == 10:
      userLoc(serialdata);
    
    if stringlenSerial != 9: 
        print "Wait line for headphones"
        print serialdata
        #time.sleep(2)
        ser.flushInput()
        ser2.flushInput()
        continue
    elif stringlenSerial2 !=2 :
        print "Wait line for belt"
        print serialdata2
        #time.sleep(2)
        ser.flushInput()
        ser2.flushInput()
        continue
    
    else:    
        sensorL = serialdata.split(" ")[2] #Left Head Sensor
        sensorR = serialdata.split(" ")[4] #Right Head Sensor
        sensor = serialdata.split(" ")[0] #Head Sensor
        sensorO = serialdata2.split(" ")[0] #Belt Sensor
        gpscheck = serialdata.split(" ")[6] #Gps Sensor

        

#############OBJECT SENSOR##############################

 	distanceO = serialdata2.split(" ")[1]
 	distanceObject = conv(distanceO)
	distance16 = callmeas(flagMeas,distanceO)
	distance2 = str(distance16)

#############FRONT SENSOR DISTANCE###########################
	distance = serialdata.split(" ")[1]
	distanceFront = conv(distance)
        distance15 = callmeas(flagMeas,distance)
        distance1 = str(distance15)#converting distance to string for tts
############LEFT SENSOR DISTANCE#################################       
	distanceL = serialdata.split(" ")[3]
        distanceL = float(distanceL) #make distance a float
        #distanceL = distanceL/12  #converting inches to feet

############RIGHT SENSOR DISTANCE#############################
	distanceR = serialdata.split(" ")[5]
        distanceR = float(distanceR) #make distance a float
        #distanceR = distanceR/12  #converting inches to feet


		
	print serialdata #Print Sensor and Distance Data from Arduino
	print serialdata2 #Printing object sensor data
        if distanceFront < 10 and distanceFront > 0: #between 10-5ft
          if wallElapsed == 0:
            say("Wall in")
            say(distance1)
            flagmeascheck(flagMeas)
            wallTimerStart = time.time()
            wallElapsed = 1
          else:
            wallElapsed = time.time() - wallTimerStart
            if wallElapsed > timerSeconds:
              wallElapsed = 0
        
#####################OBJECT SENSOR##############################################################

        if distanceObject < 8 and distanceObject > 0 : #between 8-5ft
          if objectElapsed == 0:
            say("Object in")
            say(distance2)
            flagmeascheck(flagMeas)
            objectTimerStart = time.time()
            objectElapsed = 1
          else:
            objectElapsed = time.time() - objectTimerStart
            if objectElapsed > timerProximity:
              objectElapsed = 0
	if distanceL > 144 and distanceR > 144   :
          if openingBothElapsed == 0:
            say("Opening on the right and Left")
            openingBothTimerStart = time.time()
            openingBothElapsed = 1
          else:
            openingBothElapsed = time.time() - openingBothTimerStart
            if openingBothElapsed > timerSeconds:
              openingBothElapsed = 0
	if distanceL > 144 and distanceR < 120 :
          if openingLeftElapsed == 0:
            say("Opening on the Left")
            openingLeftTimerStart = time.time()
            openingLeftElapsed = 1
          else:
            openingLeftElapsed = time.time() - openingLeftTimerStart
            if openingLeftElapsed > timerSeconds:
              openingLeftElapsed = 0
	if distanceR > 144 and distanceL < 120 :
          if openingRightElapsed == 0:
            say("Opening on the Right")
            openingRightTimerStart = time.time()
            openingRightElapsed = 1
          else:
            openingRightElapsed = time.time() - openingRightTimerStart
            if openingRightElapsed > timerSeconds:
              openingRightElapsed = 0
	elif distanceR < 15:
          if rightProximityElapsed == 0:
            say("Right wall proximity")
            rightProximityTimerStart = time.time()
            rightProximityElapsed = 1
          else:
            rightProximityElapsed = time.time() - rightProximityTimerStart
            if rightProximityElapsed > timerProximity:
              rightProximityElapsed = 0
        elif distanceL < 15:
          if leftProximityElapsed == 0:
            say("Left wall proximity")
            leftProximityTimerStart = time.time()
            leftProximityElapsed = 1
          else:
            leftProximityElapsed = time.time() - leftProximityTimerStart
            if leftProximityElapsed > timerProximity:
              leftProximityElapsed = 0

