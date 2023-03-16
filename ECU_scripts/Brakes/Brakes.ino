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

struct can_frame canMsg;
MCP2515 mcp2515(10);


void setup() {
  Serial.begin(500000);

  // Initialize LED
  pinMode(LED0, OUTPUT);
  digitalWrite(LED0, LOW);

  // Initialize CAN Message
  canMsg.can_id  = 0x001;
  canMsg.can_dlc = 8;
  canMsg.data[0] = 0;  // Brake Rate
  canMsg.data[1] = 0;
  canMsg.data[2] = 0;
  canMsg.data[3] = 0;
  canMsg.data[4] = 0;
  canMsg.data[5] = 0;
  canMsg.data[6] = 0;
  canMsg.data[7] = 0; // Manual (0) or Automatic (1)
  
  // Set MCP2515 settings
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
  mcp2515.setConfigMode();
  mcp2515.setFilterMask(MCP2515::MASK0, false, 0x7FF);
  mcp2515.setFilterMask(MCP2515::MASK1, false, 0x7FF);
  mcp2515.setFilter(MCP2515::RXF1, false, 0x102);
  mcp2515.setNormalMode();
  
  // Print Header for data receiving
  Serial.println("------- CAN Read ----------");
  Serial.println("ID  DLC   DATA");
}

void loop() {
  // Read Sensor Value from Brake Potentiometre
  int brakeSensorValue = analogRead(A0);

  // Listen for any CAN Messages in the CAN Bus
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

  // Convert sensor value from analog to digital
  int brake = convertSensorValue(brakeSensorValue);  

  /*
    Send Brake Signal to the Motor ECU    
  */ 
  if(brake > 0) {
    canMsg.data[0] = brake;
    // mcp2515.sendMessage(&canMsg);
    Serial.print("Brake: ");
    Serial.print(brake);
    Serial.print(", ");
    Serial.println("Message Sent");  
    mcp2515.sendMessage(&canMsg);  
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

// Toggling the brake lights
void toggleLights() {
    return;
}

// Calculate the brake distance
int brakeDistance(int currDistance, int targetDistance) {
  return abs(targetDistance - currDistance);
}

// Calculate the rate of deceleration (a = (v^2 - u^2) / 2s)
int brakeRate(int currSpeed, int targetSpeed, int brakeDistance) {
    return abs((targetSpeed^2 - currSpeed^2) / (2 * brakeDistance));
}

// Apply brakes based on the brake rate calculated
void applyBrakes(int rate) {
    return;
}
