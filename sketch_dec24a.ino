#include <Servo.h>

Servo servoX;  
Servo servoY;  

const int pinX = 9;
const int pinY = 10;
int valX;
int valY;

void setup() {
  servoX.attach(pinX);
  servoY.attach(pinY);

  Serial.begin(115200);
  Serial.println("System Initialized");
  Serial.println("Moving to Center (90 degrees)...");

  
  servoX.write(90);
  servoY.write(90);
  delay(2000); 
}

void loop() {
  if (Serial.available()>=2){
    valX=Serial.read();
    valY=Serial.read();
    if (valX >= 0 && valX <= 180 && valY >= 0 && valY <= 180) {
      servoX.write(valX);
      servoY.write(valY);
    }

  
    
    
  }
  
 
}
