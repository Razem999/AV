#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <SPI.h>
#include <mcp2515.h>

struct can_frame canMsgTX;
struct can_frame canMsgRX;
MCP2515 mcp2515(10);
bool automated = false;


void setup() {
  canMsgTX.can_id  = 0x003;
  canMsgTX.can_dlc = 8;
  canMsgTX.data[0] = 0;
  canMsgTX.data[1] = 0;
  canMsgTX.data[2] = 0;
  canMsgTX.data[3] = 0;
  canMsgTX.data[4] = 0;
  canMsgTX.data[5] = 0;
  canMsgTX.data[6] = 0;
  canMsgTX.data[7] = 0;

  while(!Serial);
  Serial.begin(500000);
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
  mcp2515.setConfigMode();
  mcp2515.setFilterMask(MCP2515::MASK0, false, 0x7FF);
  mcp2515.setFilterMask(MCP2515::MASK1, false, 0x7FF);
  mcp2515.setFilter(MCP2515::RXF0, false, 0x103);
  mcp2515.setNormalMode();
  
  Serial.println("Example: Write to CAN");
}

void loop() {
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

  int sensorValue = analogRead(A0);
  if (canMsgRX.can_id == 0x103 && canMsgRX.data[7] == 1) {
    canMsgRX.can_id = 0;
    canMsgTX.data[7] = 1;
    automate(canMsgRX.data[0]);
    Serial.println("here");
  } else if (!automated) {
    canMsgTX.data[7] = 0;
    canMsgRX.can_id = 0;
    manual(sensorValue);
  }
}

void automate(int speedRX) {
    canMsgTX.data[0] = speedRX;
    mcp2515.sendMessage(&canMsgTX);
}

void manual(int sensorValue) {
  int speed = map(sensorValue,200,1023,0,255);
  if (speed > 0) {
    canMsgTX.data[0] = speed;
    mcp2515.sendMessage(&canMsgTX);
    Serial.println(sensorValue);
  }
}

