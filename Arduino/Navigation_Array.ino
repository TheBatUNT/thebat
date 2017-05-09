#include <TinyGPS++.h>
#include <SoftwareSerial.h>
/*
This code reads the Analog Voltage output from the
LV-MaxSonar sensors
If you wish for code with averaging, please see
playground.arduino.cc/Main/MaxSonar
Please note that we do not recommend using averaging with our sensors.
Mode and Median filters are recommended.
*/
/*
  This code also uses TinyGPS++ liabrary to get lat and long
  from adafruit gps
 */

//Define GPS pins and boadrate
static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;
//Define gps object
TinyGPSPlus gps;
// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);

const int anPin1 = 0;
const int anPin2 = 1;
const int anPin3 = 2;
int digPin6 = 6, i=0,x = 0,num = 0;
int distance1, distance2, distance3;

const int sample = 5;// define number of samples when taking a reading -- min 3
const int error = 5;// the number of inches between values that the sample fuction will read as the same
int sum1[sample];
int sum2[sample];
int sum3[sample];
void setup() {
  Serial.begin(9600);  // sets the serial port to 9600
  pinMode(digPin6, OUTPUT);
  ss.begin(GPSBaud);
}

void start_sensor(){
  digitalWrite(digPin6,HIGH);
  delay(1);
  digitalWrite(digPin6,LOW);
}

void calibrate(){
  float samples = 5;
  float latitude = 0;
  float longitude = 0;
  Serial.print(F("UP ")); 
  
  if (gps.location.isValid())
  {
    for(i=0;i<samples;i++){
      latitude = latitude + gps.location.lat();
      longitude = longitude + gps.location.lng();
      delay(1000);
    }
  }
  else
  {
    Serial.print(F("INVALID"));
  }
  Serial.print(latitude/samples, 6);
  Serial.print(" ");
  Serial.print(longitude/samples, 6);
  Serial.print(" ");
  
}
void read_sensors(){
  /*
  Scale factor is (Vcc/512) per inch. A 5V supply yields ~9.8mV/in
  Arduino analog pin goes from 0 to 1024, so the value has to be divided by 2 to get the actual inches
  */  

  distance1 = 0;
  distance2 = 0;
  distance3 = 0;
  
   for(i=0;i<sample;i++){
     sum1[i] = analogRead(anPin1)/2;
     delay(50);
     sum2[i] = analogRead(anPin2)/2;
     delay(50);
     sum3[i] = analogRead(anPin3)/2;
     delay(50); //This is the equivant of the amount of sensors times 50.  If you changed this to 5 sensors the delay would be 250.
   }
  
  

  distance1 = mode(sum1);
  distance2 = mode(sum2);
  distance3 = mode(sum3);
    
}

int mode(int a[]) {
  
   int maxValue = 0, maxCount = 0, i, j;

   for (i = 0; i < sample; ++i) {
      int count = 0;
      
      for (j = 0; j < sample; ++j) {
         if (a[j]<= a[i] + error && a[j]>= a[i] - error)
         ++count;
      }
      
      if (count > maxCount) {
         maxCount = count;
         maxValue = a[i];
      }

   }

  return maxValue;
 
}
void print_all(){

  if(distance1 <= 200){
    Serial.print("SF ");
    Serial.print(distance1);// In inches
    Serial.print(" ");
    //Serial.println();
  }
  else{
    Serial.print("SF ");
    Serial.print(0);// In inches
    Serial.print(" ");
  }
  if(distance2 >= 100){
    Serial.print("SL ");
    Serial.print(distance2);// In inches
    Serial.print(" ");
    //Serial.println();
  }
  else{
    Serial.print("SL ");
    Serial.print(0);// In inches
    Serial.print(" ");
  }
  if(distance3 >= 100){
    Serial.print("SR ");
    Serial.print(distance3);// In inches
    Serial.print(" ");
    //Serial.println();
  }
  else{
    Serial.print("SR ");
    Serial.print(0);// In inches
    Serial.print(" ");
  }
}
//Print gps lat and long
void print_gps(){
Serial.print(F("LC ")); 
  if (gps.location.isValid())
  {
    Serial.print(gps.location.lat(), 6);
    Serial.print(F(" "));
    Serial.print(gps.location.lng(), 6);
  }
  else
  {
    Serial.print(F("INVALID"));
  }
  //Serial.print(" ");
  //Serial.println();
  
}//end print_gps


//Read gps Lat and long
void read_gps(){
  while(true){
  while (ss.available() > 0)
    if (gps.encode(ss.read())){
      //gps.encode(ss.read());
      print_gps();
      return;
    }
   
  if (millis() > 5000 && gps.charsProcessed() < 10)
  {
    Serial.println(F("No GPS detected: check wiring."));
  }

  }
}//end read_gps


void loop() {
  start_sensor();
  read_sensors();
  if(Serial.available())
  {
    x=(Serial.read()-'0');
  }
  if(x == 1)
  {
    print_all();
    calibrate();
    x=0;
  }
  else
  {
    print_all();
    read_gps();
  }
  
  Serial.println();
}
