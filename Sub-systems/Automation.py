
# Vehicle class keeps track of the vehicle's state
class vehicle:
    def __init__(self, speed, x_position, y_position, x_steering, y_steering):
        self.speed: 0
        self.x_position: 0
        self.y_position: 0
        self.x_steering: 0
        self.y_steering: 0


# Object class keeps track of the object's state
class object:
    def __init__(self, speed, x_position, y_position):
        self.type = ["car", "person"]
        self.speed: 0
        self.x_position: 0
        self.y_position: 0

# Assuming speed limit of this road is 80km/h
# Instructions are prioritized here


def prioritizeInstructions():
    return False

# Initialize Automated Vehicle Settings


def initialize():
    # Vehicle Speed

    # Vehicle Position (x, y)

    # Vehicle Steering Angle (x)

    return False

# Check Surroundings (This will be looping)


def checkSurrounding():
    # Object Detected/in range
    return False

# Procedures when object detected


def objectDetected():
    # Identify Object

    # Based on Object, Call appropriate function

    return False

# Procedure when person detected


def personDetected(distanceFromObject):
    temp = distanceFromObject
    # If person is too close, apply emergencyBrakes
    emergencyBrakes()

    # If person is far, apply brakes gracefully
    return False

# Procedure when vehicle detected


def vehicleDetected(distanceFromObject):
    # If vehicle ahead is too close and stationary, apply emergencyBrakes
    emergencyBrakes()

    # If vehicle ahead is close and moving, adjust speed to match the vehicle ahead

    # If vehicle is far, catch up to vehicle

    # If vehicle is travelling slower than speed limit, manuever to overtake
    return False

# Procedure for emergencies


def emergencyBrakes():
    return False

# Calculate speed of vehicle ahead


def calculateLeadingSpeed(vspeed, vxposition, vyposition):
    return False
