
void setup(){
    Serial.begin(9600);

    while(!Serial){
      ;//wait for connection
    }
}

const char TERMINATOR = '|';

void loop(){
// waiting for command from jetson

  if (Serial.available()>0){
    //char message buffer[32]
    // int size =serial.readBytestUntil('\n', messageBuffer, 32)
    String commandFromJetson= Serial.readStringUntil(TERMINATOR);

  //confrim
  String ackMsg = "Hello Jetson! This is what I got from you: " + commandFromJetson;

  Serial.print(ackMsg);
  //serial.flush();
  }
  delay(500);
}