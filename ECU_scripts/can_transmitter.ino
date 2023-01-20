#include <SPI.h>
#include <mcp2515.h>

struct can_frame canMsg1;
MCP2515 mcp2515(10);

#define BUTTON 2

int buttonState = 0;

void setup() {
  pinMode(BUTTON, INPUT);

  canMsg1.can_id  = 0x036;
  canMsg1.can_dlc = 8;
  canMsg1.data[0] = buttonState;  // Lights (0 is OFF, 1 is ON)
  canMsg1.data[1] = 2;
  canMsg1.data[2] = 3;
  canMsg1.data[3] = 4;
  canMsg1.data[4] = 5;
  canMsg1.data[5] = 6;
  canMsg1.data[6] = 7;
  canMsg1.data[7] = 8;
  
  while (!Serial);
  Serial.begin(9600);
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
  mcp2515.setNormalMode();
  
  Serial.println("Example: Write to CAN");
}

void loop() {
  buttonState = digitalRead(BUTTON);

  if (buttonState == HIGH) {
    canMsg1.data[0] = 1;
    mcp2515.sendMessage(&canMsg1);
    Serial.println("Button On sent");
  }
  else {
    canMsg1.data[0] = 0;
    // mcp2515.sendMessage(&canMsg1);
    Serial.println("Button Off sent");
  }
  
  delay(1000);
}
