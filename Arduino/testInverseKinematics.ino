/*
  takethesponge.ino

 This example commands to the Braccio to take a sponge from the table and it shows to the user

 Created on 18 Nov 2015
 by Andrea Martino

 This example is in the public domain.
*/

#include <Braccio.h>
#include <Servo.h>
# include <InverseK.h>


Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

Link baseLink, upperarmLink, forearmLink, handLink;



void setup() {  

   Serial.begin(9600);

   while(!Serial && millis() < 5000) {
    //Wait up to 5 sec for USB to connect 
    }
    Serial.println("Hello!");
   //Links initialization for Inverse Kinematics calculation
   baseLink.init(74, b2a(0.0), b2a(180.0));
   upperarmLink.init(125, b2a(15.0), b2a(165.0));
   forearmLink.init(125, b2a(0.0), b2a(180.0));
   handLink.init(195, b2a(0.0), b2a(180.0));
   InverseK.attach(baseLink, upperarmLink, forearmLink, handLink);

  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees
  Braccio.begin();
  

}

void loop() {
  /*
  Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
  M1=base degrees. Allowed values from 0 to 180 degrees
  M2=shoulder degrees. Allowed values from 15 to 165 degrees
  M3=elbow degrees. Allowed values from 0 to 180 degrees
  M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
  M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
  M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  */
  float m1, m2, m3, m4,m5, m6, a1, a2, a3, a4;

  float x, y, z;

  x = 0;
  y = 0;
  z = 0;

  Serial.println("Enter X position in mm");  
  while (Serial.available() == 0) {}  
  x = Serial.readString().toFloat();  
  Serial.print(x); 
  Serial.println("");  
  delay(10);

  Serial.println("Enter Y position in mm");  
  while (Serial.available() == 0) {}  
  y = Serial.readString().toFloat();  
  Serial.println("Y  in mm");
  Serial.print(y); 
  Serial.println(""); 
  delay(10);

  Serial.println("Enter Z position in mm");  
  while (Serial.available() == 0) {}  
  z = Serial.readString().toFloat();  
  Serial.println("Z in mm");
  Serial.print(z); 
  Serial.println(""); 
  delay(10);
  
   // Calculates the angles without considering a specific approach angle
  
  if(InverseK.solve(x, y, z, a1, a2, a3, a4)) {
    Serial.print(a2b(a1)); Serial.print(',');
    Serial.print(a2b(a2)); Serial.print(',');
    Serial.print(a2b(a3)); Serial.print(',');
    Serial.println(a2b(a4));
  } else {
    Serial.println("No solution found!");
  }

  m1 = a2b(a1);
  m2 = a2b(a2);
  m3 = a2b(a3);  
  m4 = a2b(a4);

  m5 = 90;
  m6 = 40;  
  Serial.println("Braccio position");
  Serial.println(m1);  Serial.print(',');
  Serial.println(m2);  Serial.print(',');
  Serial.println(m3);  Serial.print(',');
  Serial.println(m4);  Serial.print(',');
  //Starting position
                      //(step delay  M1 , M2 , M3 , M4 , M5 , M6);
  Braccio.ServoMovement(20,           m1, m2,  m3,  m4,  m5,  m6);
  
  //Wait 5 second
  delay(5000);


}

// Quick conversion from the Braccio angle system to radians
float b2a(float b){
  return b / 180.0 * PI - HALF_PI;
}

// Quick conversion from radians to the Braccio angle system
float a2b(float a) {
  return (a + HALF_PI) * 180 / PI;
}

void SerialClear(){
  
}
