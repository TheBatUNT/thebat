const int sensor1 = 3;
int distance1;
int i=0,x = 0,num = 0;
int sum1[100];


int sample = 12;// define number of samples when taking a reading -- min 3
int error = 5; // the % between values that the sample fuction will read as the same

void setup() {
  Serial.begin (9600);
  pinMode(sensor1,INPUT);
}
void calibrate(){
  /*
  Serial.print("C0");
  Serial.println();
 // digitalWrite(anPin2,LOW);
  delay(1000);
//  digitalWrite(anPin2,HIGH);
  read_sensors();

  x = 0;
  */
}


void read_sensors(){
  //Scale factor is (Vcc/512) per inch. A 5V supply yields ~9.8mV/in
  //Arduino analog pin goes from 0 to 1024, so the value has to be divided by 2 to get the actual inches
//----Read sensors------------------------------------------------ 

  distance1 = 0;
  num = 0;
  for(i=0;i<sample;i++){
  sum1[i] = (analogRead(sensor1)/2);
  delay(50);
  }
//----Sample sensor 1------------------------------------------------ 
//Check samples by groups of 3. If the samples are within the % error of eachother they are averaged 
//  and added to the sample distance.
/*
  for(i=0;i<sample;i=i+3){
  if( (sum1[i] - (sum1[i] + error)) <= sum1[i+1] && (sum1[i] + (sum1[i] + error)) >= sum1[i+1]){
    distance1 = distance1 + ((sum1[i] + sum1[i+1])/2);
    num++;
  }
  
  if( (sum1[i+1] - (sum1[i+1] + error)) <= sum1[i+2] && (sum1[i+1] + (sum1[i+1] + error)) >= sum1[i+2]){
    distance1 = distance1 + ((sum1[i+1] + sum1[i+2])/2);
    num++;  
  }
  
  if( (sum1[i] - (sum1[i] + error)) <= sum1[i+2] && (sum1[i] + (sum1[i] + error) >= sum1[i+2])){
    distance1 = distance1 + ((sum1[i] + sum1[i+2])/2);
    num++;   
    }
  }
  //Take the average of the parts of the sample that are closet together.
  if(num > 0){
    distance1 = distance1/num;
  }
  else{
    read_sensors();
  }
*/
   int maxValue = 0, maxCount = 0, j = 0;

   for (i = 0; i < sample; ++i) {
      int count = 0;
      
      for (j = 0; j < sample; ++j) {
         if (sum1[j]<= sum1[i] + error && sum1[j]>= sum1[i] - error)
         ++count;
      }
      
      if (count > maxCount) {
         maxCount = count;
         distance1 = sum1[i];
      }

   }


 


}

void print_all(){
  if(distance1 <= 200){
  Serial.print("SB ");
  Serial.print(distance1);// in feet
  Serial.println();
  }
  else{
  Serial.print("SB ");
  Serial.print("0");// in feet
  Serial.println();
  }
  
 
}
void loop() {
  read_sensors();
  if(Serial.available())
  {
    x=(Serial.read()-'0');
  }
  if(x == 1 || distance1 == 0)
  {
    calibrate();
  }
  else
  {
    print_all();
  }

 
}

