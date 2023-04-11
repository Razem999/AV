#include <SPI.h>
#include <mcp2515.h>

#define enB 3
#define in3 5
#define in4 4

struct can_frame canMsgTX;
struct can_frame canMsgRX;
MCP2515 mcp2515(10);

int rotDirection = 0;
int defaultSpeed = 40;
int speed = 0;
int storeSpeed = 0;
bool automated = false;
bool toggle = false;

void setup() {
  Serial.begin(500000);

  // Initialize CAN Message
  canMsgTX.can_id  = 0x004;
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
  // mcp2515.setFilter(MCP2515::RXF1, false, 0x101);
  // mcp2515.setFilter(MCP2515::RXF1, false, 0x103);
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

  if (canMsgRX.can_id == 0x003 && canMsgRX.data[7] == 1) {
    storeSpeed = canMsgRX.data[0];
    automated = true;
    canMsgTX.data[0] = storeSpeed;
    canMsgTX.data[7] = 1;
    mcp2515.sendMessage(&canMsgTX);
    
  } 
  // else if (canMsgRX.can_id == 0x101) {
  //   storeSpeed = canMsgRX.data[0];
  //   automated = true;
  //   speed = calculateNewSpeed(canMsgRX.data[0], speed);
  //   canMsgTX.data[0] = storeSpeed;
  //   canMsgTX.data[7] = 1;
  //   mcp2515.sendMessage(&canMsgRX);
  //   analogWrite(enB, speed);
  //   storeSpeed = speed;
  //   automated = false;
  //   canMsgTX.data[7] = 0;
  //   canMsgRX.can_id = 0;
  // }

  if (canMsgRX.can_id == 0x001) {
    // Extract data from the message and use it to control the motor speed
    speed = calculateNewSpeed(canMsgRX.data[0], storeSpeed);
    analogWrite(enB, speed);
    storeSpeed = speed;
    automated = false;
    canMsgTX.data[7] = 0;
    canMsgTX.data[0] = storeSpeed;
    mcp2515.sendMessage(&canMsgTX);
    if (canMsgRX.data[7] != 1) {
      toggle = false;    
    }    

  } else if (canMsgRX.can_id == 0x003) {
    storeSpeed = canMsgRX.data[0] + defaultSpeed;
    analogWrite(enB, storeSpeed);
    canMsgTX.data[0] = storeSpeed;
    mcp2515.sendMessage(&canMsgTX);
    toggle = false;

  } else if (!toggle && canMsgRX.data[7] == 0) {
    Serial.println("HI");
    toggle = true;
    storeSpeed = defaultSpeed;
    analogWrite(enB, defaultSpeed);
    canMsgTX.data[0] = storeSpeed;
    mcp2515.sendMessage(&canMsgTX);
    mcp2515.sendMessage(&canMsgTX);
    
  } else {
    
  }

  canMsgRX.can_id = 0;
  // Serial.println(storeSpeed);

}

int calculateNewSpeed(int brakeReceived, int currSpeed) {
  int brakeRate = (brakeReceived * 0.01) * currSpeed;
  int newSpeed = currSpeed - brakeRate;
  Serial.println(newSpeed);
  if (newSpeed < 6) {
    return 0;
  } else {
    return newSpeed;
  }
  
}

