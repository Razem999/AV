#include <Servo.h>
/*SERVO*/
/*JOYSTICK IS PIN 3*/
Servo steering_joystick;
Servo steering_servo;

/*JOYSTICK PARAMETERS*/
int JoyStick_X = 0; // FAR RIGHT 8-11,MIDDLE ABOUT 504-508,FAR LEFT 1017-1021


  void setup() 
{
  /*JOYSTICK PARAMETERS*/
  Serial.begin(9600); // 9600 bps

  /*SERVO*/
  steering_servo.attach(5);
}
void loop() 
{
  int x,y,z;
  x=analogRead(JoyStick_X);
  Serial.print(x ,DEC);
  Serial.print(", ");

  int joystick_reading = map(x,9,1020,0,180);
  Serial.print(joystick_reading);
  Serial.println();
  steering_servo.write(joystick_reading);
  
  delay(100);


   steering_servo.write(0);
}
