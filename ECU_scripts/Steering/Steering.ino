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

// Wheel needs to be centered when driving in a straight line
void wheelCentering()
{
    return;
}

// The turning angle the vehicle needs to take to make a turn
void rotateWheel(int angle)
{
    return;
}

// Toggling the left indicator lights
void toggleLeftIndicator()
{
    return;
}

// Toggling the right indicator lights
void toggleRightIndicator()
{
    return;
}
