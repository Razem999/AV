import can

# Create a CAN bus instance using the socketcan backend
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Create an empty list to store the CAN messages
can_dump = []

# Read in the CAN messages and store them in the can_dump list
while True:
    message = bus.recv()
    can_dump.append(message)
