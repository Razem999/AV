#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <SPI.h>
#include <mcp2515.h>

#define LED0 3
#define SENSOR_MAX 555
#define SENSOR_MIN 295
#define MOTOR_MAX 255
#define MOTOR_MIN 0

struct can_frame canMsgTX;
struct can_frame canMsgRX;
MCP2515 mcp2515(10);


void setup() {
  Serial.begin(500000);

  // Initialize LED
  pinMode(LED0, OUTPUT);
  digitalWrite(LED0, LOW);

  // Initialize CAN Message
  canMsgTX.can_id  = 0x001;
  canMsgTX.can_dlc = 8;
  canMsgTX.data[0] = 0;  // Brake Rate
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
  mcp2515.setFilter(MCP2515::RXF1, false, 0x101);
  mcp2515.setNormalMode();
  
  // Print Header for data receiving
  Serial.println("------- CAN Read ----------");
  Serial.println("ID  DLC   DATA");
}

void loop() {
  // Read Sensor Value from Brake Potentiometre
  int brakeSensorValue = analogRead(A0);

  // Listen for any CAN Messages in the CAN Bus
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

  // Convert sensor value from analog to digital
  int brake = convertSensorValue(brakeSensorValue);  

  /*
    Send Brake Signal to the Motor ECU    
  */ 
  if(brake > 0) {
    canMsgTX.data[0] = brake;
    // mcp2515.sendMessage(&canMsg);
    Serial.print("Brake: ");
    Serial.print(brake);
    Serial.print(", ");
    Serial.println("Message Sent");  
    mcp2515.sendMessage(&canMsgTX);  
  } else if (canMsgRX.can_id == 0x101) {
    canMsgTX.data[0] = canMsgRX.data[0];
    canMsgTX.data[7] = 1;
    canMsgRX.can_id = 0;
    mcp2515.sendMessage(&canMsgTX);
    Serial.println("Sending");
  }
  
}

int convertSensorValue(int sensorValue) {
  int rawBrakeValue = map(sensorValue,SENSOR_MIN,SENSOR_MAX,MOTOR_MIN,MOTOR_MAX);
  if(rawBrakeValue < MOTOR_MIN) {
    return 0;
  }
  else if(rawBrakeValue > MOTOR_MAX) {
    return 100;
  }
  return map(rawBrakeValue,MOTOR_MIN,MOTOR_MAX,0,20);
}
