#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Listen to messages that are being transmitted through the CAN Bus
void listeningState()
{
    processMessage();
}

// Process the message if the message is meant for this ECU
void processMessage()
{
    return;
}

// Vehicle Acceleration
int accelerate(int currSpeed, int targetSpeed, int accelerateTime)
{
    return (currSpeed - targetSpeed) / accelerateTime;
}