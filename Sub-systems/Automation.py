# Assuming speed limit of this road is 80km/h
# Vehicle class keeps track of the vehicle's state
class vehicle:
    def __init__(self, speed, x_position, y_position, x_steering, sensor_range, mode):
        self.speed: speed                   # Vehicle Speed
        self.x_position: x_position         # Vehicle Position (x)
        self.y_position: y_position         # Vehicle Position (y)
        self.x_steering: x_steering         # Vehicle Steering Angle (x)
        self.sensor_range: sensor_range     # Vehicle Sensor Range
        # Vehicle in Manual (0) or Automatic (1)
        self.mode: mode


# Object class keeps track of the object's state
class object:
    def __init__(self, speed, x_position, y_position):
        self.type = ["car", "person"]
        self.speed: 0
        self.x_position: 0
        self.y_position: 0


# Main Automation method
def automation():
    # Initialize Automated Vehicle (Tabby) settings
    speed = 60
    x_position = 0
    y_position = 0
    x_steering = 0
    sensor_range = 150
    mode = 1
    tabby = vehicle(speed, x_position, y_position,
                    x_steering, sensor_range, mode)

    while(tabby.mode == 1):
        checkSurrounding()


# Instructions are prioritized here


def prioritizeInstructions():
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


initialize()
print(vehicle.speed)
