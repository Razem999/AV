#include <SPI.h>
#include <mcp2515.h>

#define enB 3
#define in3 5
#define in4 4

struct can_frame canMsgTX;
struct can_frame canMsgRX;
MCP2515 mcp2515(10);

int rotDirection = 0;

void setup() {
  Serial.begin(500000);

  // Initialize CAN Message
  canMsgTX.can_id  = 0x01;
  canMsgTX.can_dlc = 8;
  canMsgTX.data[0] = 0;  // Rate
  canMsgTX.data[1] = 0;
  canMsgTX.data[2] = 0;
  canMsgTX.data[3] = 0;
  canMsgTX.data[4] = 0;
  canMsgTX.data[5] = 0;
  canMsgTX.data[6] = 0;
  canMsgTX.data[7] = 0; // Manual (0) or Automatic (1)

  // Set Message Transmission settings
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
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
  int pwmOutput = 255;
  if (canMsgRX.id == 0x010) {
    // Extract data from the message and use it to control the motor speed
    int braking = canMsgRX.data[0]*0.01
    int brake = braking * pwmOutput

    analogWrite(enB, brake)

  }else{
    //int potValue = 500; // Read potentiometer value
    // int pwmOutput = map(potValue, 0, 1023, 0, 255); // Map the potentiometer value from 0 to 255
    
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    // delay(2000);
    
    analogWrite(enB, canMsgRX.data[3]);
    Serial.print("I am speed ");
    Serial.println(canMsgRX.data[3]);
    // delay(200);
  }

  
  
}

void motor() {
  // int potValue = analogRead(A0); // Read potentiometer value
  // int pwmOutput = map(potValue, 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  // analogWrite(enA, pwmOutput); // Send PWM signal to L298N Enable pin

  int potValue = 100; // Read potentiometer value
  int pwmOutput = 255; // Map the potentiometer value from 0 to 255
  analogWrite(enB, pwmOutput); // Send PWM signal to L298N Enable pin

  // If button is pressed - change rotation direction
  if (true) {
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    rotDirection = 1;
    delay(20);
    Serial.println("I spin now!");
  }
}