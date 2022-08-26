/*
 * Firmata is a generic protocol for communicating with microcontrollers
 * from software on a host computer. It is intended to work with
 * any host computer software package.
 *
 * To download a host software package, please click on the following link
 * to open the list of Firmata client libraries in your default browser.
 *
 * https://github.com/firmata/arduino#firmata-client-libraries
 */

/* This firmware supports as many servos as possible using the Servo library
 * included in Arduino 0017
 *
 * This example code is in the public domain.
 */

#include <Servo.h>
#include <Firmata.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <Braccio.h>
#include <Servo.h>
# include <InverseK.h>

LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display
Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

//Current position of the Braccio Arm in mm
float x, y, z; 

//Braccio Servos motors angle position
float m1, m2, m3, m4,m5, m6;

Link baseLink, upperarmLink, forearmLink, handLink;


void PerformInverseKinematics(float x,float y,float z)
{ 
  float a1, a2, a3, a4;
  lcd.clear();
  lcd.setCursor(1,0);

  if(InverseK.solve(x, y, z, a1, a2, a3, a4)) {
    lcd.print("Solution found!");
  } else {
    lcd.print("No solution found!");
    return;
  }

  m1 = a2b(a1);
  m2 = a2b(a2);
  m3 = a2b(a3);  
  m4 = a2b(a4);


                       //(step delay  M1 , M2 , M3 , M4 , M5 , M6);
  Braccio.ServoMovement(20,           m1, m2,  m3,  m4,  m5,  m6);

    //Wait 3 second
  delay(3000);
  
}


void stringCallback(char *msg)
{ 
  char command;

  lcd.clear();
  lcd.setCursor(1,0);
  lcd.print(msg);
  delay(2);
  lcd.clear();

  String data = String(msg);

  command = data.charAt(0);
  data.remove(0,1);

  switch (command)
  {

   case 'x':
   {
      x = data.toFloat();
      String inputx = "x = " + String(x);
      lcd.setCursor(2,0);
      lcd.print(inputx);
      break;
    }
     
    case 'y':
    {
      y = data.toFloat();
      String inputy = "y = " + String(y);
      lcd.setCursor(2,0);
      lcd.print(inputy);
      break;
    }

     case 'z':
     {
      z = data.toFloat();
      String inputz = "z = " + String(z);
      lcd.print(inputz);
      break;
     }

     case 'c':
     {
      PerformInverseKinematics(x,y,z);
      break;
     }

     case 'g':
     {
      lcd.print("Gripper");
      // Open/Close gripper
      m6 = data.toFloat();
      
      // Only move gripper
                      //(step delay  M1 , M2 , M3 , M4 , M5 , M6);
      Braccio.ServoMovement(20,       m1, m2,  m3,  m4,  m5,  m6);
      
      break;
     }

     case 'p':
     {
      lcd.clear();
      lcd.setCursor(1,0);
      lcd.print("x y z " + String(x));
      lcd.setCursor(2,0);
      lcd.print(String(y) + " " + String(z));
      break;
     }
      
     default:
     {
      lcd.print("Error");
     }
  }
  
  
}



void systemResetCallback()
{
  Braccio.begin();
}

void setup()
{
  Firmata.setFirmwareVersion(FIRMATA_FIRMWARE_MAJOR_VERSION, FIRMATA_FIRMWARE_MINOR_VERSION);
  // Firmata.attach(ANALOG_MESSAGE, analogWriteCallback);
  Firmata.attach(SYSTEM_RESET, systemResetCallback);
  Firmata.attach(STRING_DATA, stringCallback);

  Firmata.begin(57600);
  systemResetCallback();

  // Initiate the InverseK library for the Braccio Arm
  baseLink.init(74, b2a(0.0), b2a(180.0));
  upperarmLink.init(125, b2a(15.0), b2a(165.0));
  forearmLink.init(125, b2a(0.0), b2a(180.0));
  handLink.init(195, b2a(0.0), b2a(180.0));
  InverseK.attach(baseLink, upperarmLink, forearmLink, handLink);

  x = 0;
  y = 0;
  z = 0;
  lcd.init();
  // Print a message to the LCD.
  lcd.clear();
  lcd.backlight();

  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees
  Braccio.begin(); 
  
  lcd.print("Braccio Ready");
  

}

void loop()
{
  while (Firmata.available())
    Firmata.processInput();
}


// Quick conversion from the Braccio angle system to radians
float b2a(float b){
  return b / 180.0 * PI - HALF_PI;
}

// Quick conversion from radians to the Braccio angle system
float a2b(float a) {
  return (a + HALF_PI) * 180 / PI;
}
