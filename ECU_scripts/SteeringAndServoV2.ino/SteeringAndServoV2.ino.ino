#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <SPI.h>
#include <mcp2515.h>
#include <Servo.h>
/*SERVO*/
/*JOYSTICK IS PIN 3*/
Servo steering_joystick;
Servo steering_servo;

struct can_frame canMsgTX;
struct can_frame canMsgRX;
MCP2515 mcp2515(10);

/*JOYSTICK PARAMETERS*/
int JoyStick_X = 0; // FAR RIGHT 8-11,MIDDLE ABOUT 504-508,FAR LEFT 1017-1021


  void setup() 
{
  /*JOYSTICK PARAMETERS*/
  Serial.begin(500000);

  // Initialize CAN Message
  canMsgTX.can_id  = 0x002;
  canMsgTX.can_dlc = 8;
  canMsgTX.data[0] = 0;  // Rate
  canMsgTX.data[1] = 0;
  canMsgTX.data[2] = 0;
  canMsgTX.data[3] = 0;
  canMsgTX.data[4] = 0;
  canMsgTX.data[5] = 0;
  canMsgTX.data[6] = 0;
  canMsgTX.data[7] = 0; // Manual (0) or Automatic (1)

  // Set MCP2515 settings
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
  mcp2515.setConfigMode();
  mcp2515.setFilterMask(MCP2515::MASK0, false, 0x7FF);
  mcp2515.setFilterMask(MCP2515::MASK1, false, 0x7FF);
  mcp2515.setFilter(MCP2515::RXF0, false, 0x102);
  mcp2515.setNormalMode();

  /*SERVO*/
  steering_servo.attach(5);
}
void loop() 
{
  if (mcp2515.readMessage(&canMsgRX) == MCP2515::ERROR_OK) {
    Serial.print(canMsgRX.can_id, HEX); // print ID
    Serial.print(" "); 
    Serial.print(canMsgRX.can_dlc); // print DLC
    Serial.print(" ");
    
    for (int i = 0; i<canMsgRX.can_dlc; i++)  {  // print the data
      Serial.print(canMsgRX.data[i]);
      Serial.print(" ");
    }
    Serial.println();
  }

  int x,y,z;
  x=analogRead(JoyStick_X);
  // Serial.print(x ,DEC);
  // Serial.print(", ");

  if (canMsgRX.can_id == 0x102) {
    int joystick_reading = map(canMsgRX.data[0],0,255,0,180);
    canMsgRX.can_id = 0;
    steering_servo.write(joystick_reading);
  } else {
    int joystick_reading = map(x,9,1020,0,180);
  // Serial.print(joystick_reading);
  // Serial.println();
  steering_servo.write(joystick_reading);
  }
  
  
  delay(100);


   steering_servo.write(0);
}
