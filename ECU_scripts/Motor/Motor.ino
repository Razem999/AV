#include <SPI.h>
#include <mcp2515.h>

#define enB 3
#define in3 5
#define in4 4

int rotDirection = 0;

void setup() {
  Serial.begin(500000);
  pinMode(enB, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  // Set initial rotation direction
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void loop() {
  int potValue = 500; // Read potentiometer value
  // int pwmOutput = map(potValue, 0, 1023, 0, 255); // Map the potentiometer value from 0 to 255
  
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  delay(2000);
  
  analogWrite(enB, 30);
  Serial.print("I am speed ");
  Serial.println("20");
  delay(200);

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