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

// Toggling the brake lights
void toggleLights()
{
    return;
}

// Calculate the rate of deceleration
int brakeRate(int currSpeed, int targetSpeed, int brakeTime)
{
    return;
}

// Apply brakes based on the brake rate calculated
void applyBrakes(int rate)
{
    return;
}