#include <mcp_can.h>
#include <mcp_can_dfs.h>
#include <SPI.h>

MCP_CAN CAN(10); // replace with the SPI on Adruino 


void setup() {  
  // put your setup code here, to run once:
  
  Serial.begin(500000);
  while(CAN_OK != CAN.begin(CAN_1000KBPS)){
    Serial.println("CAN initialization failed");
    delay(100);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  byte len =8;
  byte bufin[8];
  if(CAN_MSGAVAIL == CAN.checkReceive()){
    CAN.readMsgBuf(&len, bufin);
    usigned long canID = CAN.getCanId();
    serial.println("---------------------------")
    Serial.print("Data from ID : 0x");
    Serial.println(canID ,HEX);
    for(int i = 0; i<len; i++){
      Serial.print(bufin[i]);
      Serial.print("\t");
    }
    Serial.println();    
  }
}
