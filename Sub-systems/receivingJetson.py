import can
import datetime

print("test")
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
    # print(hex(message_dict['data'][0]))
    # #print(hex(message_dict['id']))
    # #print(message_dict['timestamp'])
    # print(message_dict['id'])

    output_file= open('can_messages.txt', 'w')

    #message lsitener
    def message_listener(message):
        output_file.write(str(message)+ '\n')

    while True:
        pass

    #message listener to the bus
    #notifier = can.Notifier(bus, [message_listener])

   

    #print(f"ID:{message_dict['id']} TimeStamp:{message_dict['timestamp']}DLC:{message_dict['dlc']} Data:{message_dict['data'].hex()}")
    #print(message)
    
    if message is None:
        print('Timeout occured, no message.')



 
