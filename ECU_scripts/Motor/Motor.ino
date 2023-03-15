#include <SPI.h>
#include <mcp2515.h>

#define enB 3
#define in3 5
#define in4 4

struct can_frame canMsgTX;
struct can_frame canMsgRX;
MCP2515 mcp2515(10);

int rotDirection = 0;
int speed = 40;

void setup() {
  Serial.begin(500000);

  // Initialize CAN Message
  canMsgTX.can_id  = 0x011;
  canMsgTX.can_dlc = 8;
  canMsgTX.data[0] = 0;  // Speed
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
  mcp2515.setFilter(MCP2515::RXF0, false, 0x001);         // ID for Brakes
  mcp2515.setFilter(MCP2515::RXF1, false, 0x003);         // ID for Accelerator
  mcp2515.setNormalMode();

  // Print Header for data receiving
  Serial.println("------- CAN Read ----------");
  Serial.println("ID  DLC   DATA");

  pinMode(enB, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  // Set initial rotation direction
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
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

  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);

  if (canMsgRX.can_id == 0x001) {
    // Extract data from the message and use it to control the motor speed
    speed = calculateNewSpeed(canMsgRX.data[0], speed);
    analogWrite(enB, speed);
    canMsgRX.can_id = 0;
  } else if (canMsgRX.can_id == 0x003) {
    analogWrite(enB, canMsgRX.data[3] + speed);
    canMsgRX.can_id = 0;
  } else {
    speed = 40;
    analogWrite(enB, speed);
  }
  
  canMsgTX.data[0] = speed;
  mcp2515.sendMessage(&canMsgTX);

}

int calculateNewSpeed(int brakeReceived, int currSpeed) {
  int brakeRate = (brakeReceived * 0.01) * currSpeed;
  return currSpeed - brakeRate;
}

