#include <iostream>
#include <matlabengine.hpp>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
/*This code uses the MATLAB Engine API for C++ to start the MATLAB engine, 
load data from a file 'mydata.mat' and access its variable called 'mydata' and save it into data variable, 
and finally get the data from the data variable and use it to send it to the sensors using the can frame.*/
int main() {
    // Start the MATLAB engine
    std::unique_ptr<MATLABEngine> matlabPtr = startMATLAB();
    MATLABEngine &matlab = *matlabPtr;
    
    // Load data from a MATLAB file
    matlab.eval("data = load('mydata.mat');");
    matlab.eval("data = data.mydata;");

    // Create a socket for the CAN bus
    int sock = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if (sock < 0) {
        std::cerr << "Error creating socket" << std::endl;
        return 1;
    }

    // Bind the socket to the can0 interface
    struct ifreq ifr;
    strcpy(ifr.ifr_name, "can0");
    ioctl(sock, SIOCGIFINDEX, &ifr);

    struct sockaddr_can addr;
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;
    bind(sock, (struct sockaddr *)&addr, sizeof(addr));

    // Create a CAN frame to send
    struct can_frame frame;
    frame.can_id = 0x123;    // example identifier
    frame.can_dlc = 5;       // data length
    frame.data[0] = matlab.getVariable("data[0]");  // get data from matlab
    frame.data[1] = matlab.getVariable("data[1]");
    frame.data[2] = matlab.getVariable("data[2]");
    frame.data[3] = matlab.getVariable("data[3]");
    frame.data[4] = matlab.getVariable("data[4]");

    // Send the frame on the bus
    int bytes_sent = write(sock, &frame, sizeof(frame));
    if (bytes_sent < 0) {
        std::cerr << "Error sending frame" << std::endl;
        return 1;
    }

    close(sock);
    return 0;
}
