#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <SPI.h>
#include <mcp2515.h>

#define LED0 3
#define LED1 4

struct can_frame canMsg;
MCP2515 mcp2515(10);


void setup() {
  Serial.begin(9600);

  // Initialize LED
  pinMode(LED0, OUTPUT);
  pinMode(LED1, OUTPUT);

  digitalWrite(LED1, HIGH);
  digitalWrite(LED0, HIGH);
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
  mcp2515.setNormalMode();
  
  Serial.println("------- CAN Read ----------");
  Serial.println("ID  DLC   DATA");
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

    if (canMsg.data[0] == 0) {
      digitalWrite(LED0, LOW);
      digitalWrite(LED1, HIGH);
    }
    else {
      digitalWrite(LED0, HIGH);
      digitalWrite(LED1, LOW);
    }

    Serial.println();
  }
  
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
