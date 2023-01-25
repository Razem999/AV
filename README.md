# Autonomous Vehicle - Central Embedded System
This is a sub-project of the Tabby Evo Autonomous Vehicle.  
This repository mainly focuses on the Central Embedded System, which includes the functionality of the ECUs (Electronic Control Unit) and communication using CAN Bus.  

The ECU serves as an actuator for the vehicle, which receives instructions (formatted as CAN Message) from the CAN Transmitter.  
The CAN Bus is a communication protocol where messages are sent from one ECU to all other ECUs in the system.  

## ECU_scripts
This folder consists of ECUs that are in the vehicle. It contains the following ECUs and their functionalities:  
 - Brakes: This operates the braking system of the vehicle
 - Accelerate: This operates the accelerator of the vehicle
 - Steering: This operates the steering wheel (turning) of the vehicle

## Sub-systems
This folder consists of programs that will be running when the vehicle is in Autonomous mode. It contains the following programs and their functionalities:
 - SimulationData: This program reads sensor data from a Matlab Autonomous Vehicle scenario and sends the data to the DecisionMatrix program
 - DecisionMatrix: This program receives processed sensor data from the SensorProcessor (need to be implemented) and makes decision based on the data. This then generates instructions for the necessary ECUs and sends it to the CANTransmitter
 - ActionCentre: This takes the instructions from the DecisionMaker and formats the instructions into a CAN Message and transmit the message through the CAN Bus
