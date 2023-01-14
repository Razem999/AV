#include <stdio.h>

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

// Wheel needs to be centered when driving in a straight line
void wheelCentering()
{
    return;
}

// The turning angle the vehicle needs to take to make a turn
void rotateWheel(int angle)
{
    return;
}

// Toggling the left indicator lights
void toggleLeftIndicator()
{
    return;
}

// Toggling the right indicator lights
void toggleRightIndicator()
{
    return;
}
