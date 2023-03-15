
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <SPI.h>
#include <mcp2515.h>

struct can_frame canMsg;
MCP2515 mcp2515(10);

// BUTTON 1: RANDOM OBSTACLE
const int buttonPin1 = 2;
const int ledPin1 = 3;  
// Set up the state for obstacle button
int buttonState1 = 0; 
int ledState1 = 0;

// BUTTON 2: CAR MODE
const int buttonPin2 = 4;
const int ledPin2 = 5;  
// Set up variable for the state of the button1 
int buttonState2 = 0; 
int ledState2 = 0;

// BUTTON 3: KILL SWITCH
const int buttonPin3 = 6;
const int ledPin3 = 7;  
// Set up variable for the state of the button1 
int buttonState3 = 0; 
int ledState3 = 0;

void setup() {
  //Initialize Serial
  Serial.begin(500000);
  // Set MCP2515 settings
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
  mcp2515.setConfigMode();
  mcp2515.setFilterMask(MCP2515::MASK0, false, 0x7FF);
  mcp2515.setFilterMask(MCP2515::MASK1, false, 0x7FF);
  mcp2515.setFilter(MCP2515::RXF1, false, 0x102);
  mcp2515.setNormalMode();

  // BUTTON1: ARDUINO PIN SETTINGS
  pinMode(buttonPin1,INPUT);// It is input because the Arduino is reading from the Button
  pinMode(ledPin1,OUTPUT);// This output will come from the arduino
  // Initialize CAN Message for Button 1 : OBSTACLE
  canMsg.can_id  = 0x005;   // Obstacle button CAN_ID
  canMsg.can_dlc = 8;
  canMsg.data[0] = 0; 
  canMsg.data[1] = 0;
  canMsg.data[2] = 0;
  canMsg.data[3] = 0;
  canMsg.data[4] = 0;
  canMsg.data[5] = 0;
  canMsg.data[6] = 0;
  canMsg.data[7] = 0; // Obstacle goes off (0) or Generate random obstable (1)
  
  // BUTTON2: ARDUINO PIN SETTINGS
  pinMode(buttonPin2,INPUT);// It is input because the Arduino is reading from the Button
  pinMode(ledPin2,OUTPUT);// This output will come from the arduino
  // Initialize CAN Message for Button 2 : CAR MODE (MANUAL, AUTO)
  canMsg.can_id  = 0x006;   // Car Mode CAN_ID
  canMsg.can_dlc = 8;
  canMsg.data[0] = 0;  
  canMsg.data[1] = 0;
  canMsg.data[2] = 0;
  canMsg.data[3] = 0;
  canMsg.data[4] = 0;
  canMsg.data[5] = 0;
  canMsg.data[6] = 0;
  canMsg.data[7] = 0; // Manual mode (0), Automatic mode (1)

  // BUTTON3: ARDUINO PIN SETTINGS 
  pinMode(buttonPin3,INPUT);// It is input because the Arduino is reading from the Button
  pinMode(ledPin3,OUTPUT);// This output will come from the arduino
  // Initialize CAN Message for Button 3: KILL SWITCH
  canMsg.can_id  = 0x007;   // Kill Switch CAN_ID
  canMsg.can_dlc = 8;
  canMsg.data[0] = 0;  
  canMsg.data[1] = 0;
  canMsg.data[2] = 0;
  canMsg.data[3] = 0;
  canMsg.data[4] = 0;
  canMsg.data[5] = 0;
  canMsg.data[6] = 0;
  canMsg.data[7] = 0; // KILL SWITCH IS OFF (0), KILL SWITCH IS ON (1)
  
  // Print Header for data receiving
  Serial.println("------- CAN Read ----------");
  Serial.println("ID  DLC   DATA");
}

void loop() {
  // This will be called after the setup and will be executed infinetly
  //Serial.println(digitalRead(buttonPin1));// HIGH IF BUTTON IS PRESSED, OR LOW (VIA PULL DOWN 10KOhm RESISTOR IS BUTTON IS NOT PRESSED)
  //delay(100);
  
  //Button1: OBSTACLE BUTTON
  buttonState1 = digitalRead(buttonPin1);
  // Make condition for the Led to turn on and off
  if(buttonState1 == HIGH){
    ledState1 = !ledState1;
    digitalWrite(ledPin1, ledState1);
  }
  
  //Button2: CAR MODE BUTTON
  buttonState2 = digitalRead(buttonPin2);
  if(buttonState2 == HIGH){
    ledState2 = !ledState2;
    digitalWrite(ledPin2, ledState2);
  }

  //Button3: KILL SWITCH BUTTON
  buttonState3 = digitalRead(buttonPin3);
  if(buttonState3 == HIGH){
    ledState3 = !ledState3;
    digitalWrite(ledPin3, ledState3);
  }
  delay(50);
}
