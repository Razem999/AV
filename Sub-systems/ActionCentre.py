
# List of instructions sent from the Decision matrix will be processed here
import can #this is for to access the can bus library

#initialize global variable bus
bus = can.interface.Bus(channel='can0', bustype='socketcan')
ACK_ID= 0x456
#define ack codes
ACK_RECEIVED = 1
ACK_PROCESSED = 2

def processDecision():
    return False

# Messages directed to the ECUs are constructed here (follows the CAN Bus Frame Structure)
def constructMessage():
    class CanFrame:
        def __init__(self, data, id, dlc):
            self.data = data
            self.id = id
            self.dlc = dlc

        def to_can_msg(self):
    
            #Returns the CanFrame data as a can.Message object
        
            return can.Message(arbitration_id=self.id, data=self.data, dlc=self.dlc, is_extended_id=False)
    # Example usage:
    # Create a CanFrame instance with some data, ID and DLC
    frame = CanFrame([0x01, 0x02, 0x03, 0x04], 0x123, 8)
    # Convert the CanFrame to a can.Message object
    msg = frame.to_can_msg()
    # Send the message over the bus
    bus.send(msg)


# Check to see if the Message has been sent and received by the appropriate ECU
def ackMessage():
    #gonna edit this. but function for sending and reciving the ackmesssage
    #didn't wanna change it too much
    # modify the receive_message function
    def send_ack(bus, id, ack_code):
    #Sends an acknowledgement message over the specified bus to the ECU with the specified ID and ack code.


    # Create the acknowledgement message with the specified ID and ack code
        ack_msg = can.Message(arbitration_id=id+0x800, data=[ack_code], dlc=1, is_extended_id=False)
    # Send the acknowledgement message
        bus.send(ack_msg)
        print("Sent acknowledgement message to ECU with ID: ", id)
    def receive_message(msg):
        print("Received message with ID: ", msg.arbitration_id)
        print("Message data: ", msg.data)
        # Send an acknowledgement message with code ACK_RECEIVED to the ECU that sent the received message
        send_ack(bus, msg.arbitration_id, ACK_RECEIVED)
        # process the received message
        # ...
        # Send an acknowledgement message with code ACK_PROCESSED to the ECU that sent the received message
        send_ack(bus, msg.arbitration_id, ACK_PROCESSED)


# Transmit constructed message through the CAN Bus
def transmitMessage(bus,data,id, dlc, ack_request=False):
    # send a message with the specified data, ID, and DLC: data length code around 8 bitss
    msg = can.Message(arbitration_id=id, data=data, dlc=dlc, is_extended_id =False)
    
    #set ack flag
    msg.is_remote_frame = ack_request
    # Send the message over the bus
    bus.send(msg)
