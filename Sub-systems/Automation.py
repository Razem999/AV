# Assuming speed limit of this road is 80km/h
# Vehicle class keeps track of the vehicle's state
class vehicle:
    def __init__(self, speed, x_position, y_position, x_steering, sensor_range, width, length, mode):
        # Vehicle Speed (in km/h) Min = 0, Max = 255
        self.speed: speed
        self.x_position: x_position         # Vehicle Position x (in metres)
        self.y_position: y_position         # Vehicle Position y (in metres)
        self.x_steering: x_steering         # Vehicle Steering Angle (x)
        self.sensor_range: sensor_range     # Vehicle Sensor Range (in metres)
        self.width: width                   # Vehicle Width (in metres)
        self.length: length                 # Vehicle Length (in metres)
        # Vehicle must maintain this Safety Distance while driving at high speeds
        self.safety_distance_driving: 10
        self.safety_distance_stationary: 3
        self.safety_pedestrian: 20
        # Vehicle in Manual (0) or Automatic (1)
        self.mode: mode


# Object class keeps track of the object's state
class object:
    def __init__(self, speed, x_position, y_position, width, length):
        self.type = []
        self.speed: speed                   # Object Speed (in km/h)
        self.x_position: x_position
        self.y_position: y_position
        self.width: width
        self.length: length


# Environment class that keeps track of vehicles and objects
class env:
    def __init__(self, vehicle):
        self.vehicle: vehicle
        self.objects = []
        self.object_type = ["vehicle", "person"]

# Main Automation method


def automation():
    # Initialize Automated Vehicle (Tabby) settings
    speed = 80
    x_position = 0
    y_position = 0
    x_steering = 0
    sensor_range = 150
    width = 2.48
    length = 4.12
    mode = 1
    tabby = vehicle(speed, x_position, y_position,
                    x_steering, sensor_range, width, length, mode)
    environment = env(tabby)

    while(tabby.mode == 1):
        checkSurrounding(environment)


# Instructions are prioritized here


def prioritizeInstructions():
    return False

# Check Surroundings (This will be looping)


def checkSurrounding(environment):
    # No Object in the Environment
    if(environment.objects is None):
        return

    # If Object Detected/in range, check object type
    # For vehicle
    if(environment.objects[0].type == environment.object_type[0]):
        vehicleDetected(environment)
        environment.objects.clear
        return

    # For pedestrian
    elif(environment.objects[0].type == environment.object_type[1]):
        personDetected(environment)
        environment.objects.clear
    return False

# Procedure when vehicle detected


def vehicleDetected(environment):
    # If vehicle ahead is close and stationary or moving very slowly, apply emergencyBrakes
    if(environment.vehicle.y_position - environment.objects[0].y_position < environment.vehicle.safety_distance_driving and
       (environment.objects[0].speed == 0 or (environment.objects[0].speed - environment.vehicle.speed > 20))):
        emergencyBrakes()

    # If vehicle ahead is close and moving, adjust speed to match the vehicle ahead
    if(environment.vehicle.y_position - environment.objects[0].y_position < environment.vehicle.safety_distance_driving and environment.objects[0].speed - environment.vehicle.speed > 0):
        for i in range(environment.vehicle.speed, (environment.objects[0].speed), -1):
            environment.vehicle.speed = i
            # send canMsg with the vehicle's speed value
            # add delay if necessary
        performManeuver(environment)

# Procedure when person detected


def personDetected(environment):
    # If person is too close, apply emergencyBrakes
    if(environment.vehicle.y_position - environment.objects[0].y_position < environment.vehicle.safety_pedestrian):
        emergencyBrakes()

    # If person is far, apply brakes gracefully
    if(environment.vehicle.y_position - environment.objects[0].y_position > environment.vehicle.safety_pedestrian):
        for i in range(environment.vehicle.speed, (environment.objects[0].speed), -1):
            environment.vehicle.speed = i
    return False


# Procedure for emergencies


def emergencyBrakes():
    # send canMsg with 100% brakes
    return False

# Calculate speed of vehicle ahead


def performManeuver(environment):
    switchToLeftLane(environment)
    # for(i = environment.vehicle.speed, i < (environment.objects[0].speed + 15), i++):
    for i in range(environment.vehicle.speed, (environment.objects[0].speed + 15), 1):
        environment.vehicle.speed = i
        # send canMsg with the vehicle's speed value

    while(True):
        if(checkIfOvertake(environment.vehicle, environment.objects[0])):
            break

    switchToRightLane(environment)


def switchToLeftLane(environment):
    while(environment.vehicle.x_position - environment.objects[0].x_position < 1.5):
        # for(i = environment.vehicle.x_position, abs(i - environment.objects[0].x_position) > 1.5, i--):
        for i in range(abs(i - environment.objects[0].x_position), 1.5, -1):
            environment.vehicle.x_position -= 1
            # send canMsg with appropriate steering angle


def switchToRightLane(environment):
    while(environment.vehicle.x_position - environment.objects[0].x_position != 0):
        # for(i = environment.vehicle.x_position, abs(i - environment.objects[0].x_position) != 0, i++):
        for i in range(abs(i - environment.objects[0].x_position) != 0, 1):
            environment.vehicle.x_position += 1
            # send canMsg with appropriate steering angle


def checkIfOvertake(veh, obj):
    if((veh.y_position - obj.y_position) > veh.safety_distance_driving):
        return True
    else:
        return False
