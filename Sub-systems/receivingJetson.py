import can
import datetime

# Create a CAN bus instance using the socketcan backend
bus = can.Bus(channel='can0', bustype='socketcan')

# Create an empty list to store the CAN messages
can_dump = []

# Read in the CAN messages and store them in the can_dump list
while True:
    message = bus.recv(1.0)
    message_dict ={
        'id': hex(message.arbitration_id),
        'data':message.data,
        "timestamp": datetime.datetime.fromtimestamp(message.timestamp),
        'dlc(datalength)': message.dlc
    }
    can_dump.append(message_dict)
    print(hex(message_dict['data'][0]))
    #print(hex(message_dict['id']))
    #print(message_dict['timestamp'])
    print(message_dict['id'])

    #print(f"ID:{message_dict['id']} TimeStamp:{message_dict['timestamp']}DLC:{message_dict['dlc']} Data:{message_dict['data'].hex()}")
    #print(message)
    # Open the output file for writing
    output_file = open('can_messages.txt', 'w')
    # Define a message listener function
    def message_listener(msg):
        # Write the message to the output file
        output_file.write(str(msg) + '\n')
    # Wait for messages
    while True:
        pass  # This loop will run forever, until the program is interrupted or stopped manually
    # Add the message listener to the bus
    notifier = can.Notifier(bus, [message_listener])
        
        if message is None:
            print('Timeout occured, no message.')



 
