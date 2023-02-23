
// #define BUTTONPIN 1;
const int buttonPin1 = 2;
const int ledPin1 = 13;  
// Set up variable for the state of the button1 
int buttonState1 = 0; 
int ledState1 = 0;

// #define BUTTONPIN 2;
const int buttonPin2 = 3;
const int ledPin2 = 12;  
// Set up variable for the state of the button1 
int buttonState2 = 0; 
int ledState2 = 0;

// #define BUTTONPIN 3;
const int buttonPin3 = 4;
const int ledPin3 = 11;  
// Set up variable for the state of the button1 
int buttonState3 = 0; 
int ledState3 = 0;


 

void setup() {
  //Initialize The setup Protocol

  //BUTTON1:
  pinMode(buttonPin1,INPUT);// It is input because the Arduino is reading from the Button
  pinMode(ledPin1,OUTPUT);// This output will come from the arduino

  //BUTTON2:
  pinMode(buttonPin2,INPUT);// It is input because the Arduino is reading from the Button
  pinMode(ledPin2,OUTPUT);// This output will come from the arduino


   //BUTTON3:
  pinMode(buttonPin3,INPUT);// It is input because the Arduino is reading from the Button
  pinMode(ledPin3,OUTPUT);// This output will come from the arduino

 
  
 // Lets print the Button being pressed
 //Serial.begin(9600);

}

void loop() {
  // This will be called after the setup and will be executed infinetly
  //Serial.println(digitalRead(buttonPin1));// HIGH IF BUTTON IS PRESSED, OR LOW (VIA PULL DOWN 10KOhm RESISTOR IS BUTTON IS NOT PRESSED)
  //delay(100);
  
  //Button1:
  buttonState1 = digitalRead(buttonPin1);
  // Make condition for the Led to turn on and off
  if(buttonState1 == HIGH){
    ledState1 = !ledState1;
    digitalWrite(ledPin1, ledState1);
  }
  
  //Button2: 
  buttonState2 = digitalRead(buttonPin2);
  if(buttonState2 == HIGH){
    ledState2 = !ledState2;
    digitalWrite(ledPin2, ledState2);
  }

  //Button3: 
  buttonState3 = digitalRead(buttonPin3);
  if(buttonState3 == HIGH){
    ledState3 = !ledState3;
    digitalWrite(ledPin3, ledState3);
  }

  

  delay(100);
  
}
