#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <SPI.h>
#include <mcp2515.h>

struct can_frame canMsg;
MCP2515 mcp2515(10);


void setup() {
  canMsg.can_id  = 0x1A;
  canMsg.can_dlc = 8;
  canMsg.data[0] = 0;
  canMsg.data[1] = 50;
  canMsg.data[2] = 100;
  canMsg.data[3] = 4;
  canMsg.data[4] = 5;
  canMsg.data[5] = 6;
  canMsg.data[6] = 7;
  canMsg.data[7] = 8;

  while(!Serial);
  Serial.begin(500000);
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
  mcp2515.setNormalMode();
  
  Serial.println("Example: Write to CAN");
}

void loop() {
  if (mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK) {
    Serial.print(canMsg.can_id, HEX); // print ID
    Serial.print(" "); 
    Serial.print(canMsg.can_dlc); // print DLC
    Serial.print(" ");
    
    for (int i = 0; i<canMsg.can_dlc; i++)  {  // print the data
      Serial.print(canMsg.data[i]);
      Serial.print(" ");
    }

    Serial.println();
  }

  int sensorValue = analogRead(A0);
  int speed = map(sensorValue,0,1023,0,255);
  canMsg.data[3] = speed;

  mcp2515.sendMessage(&canMsg);
  Serial.println("Message Sent");
//  delay(1000);
  
}

// Vehicle Acceleration
int accelerate(int currSpeed, int targetSpeed, int accelerateTime)
{
  return (currSpeed - targetSpeed) / accelerateTime;
}

void applyAccelerate(int accelerate) 
{
  
}

