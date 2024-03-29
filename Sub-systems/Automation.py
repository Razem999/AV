""" Assuming speed limit of this road is 80km/h """

import os
import can
import random

""" Vehicle class keeps track of the vehicle's state """


class Vehicle:
    def __init__(self, speed, x_position, y_position, x_steering, sensor_range, width, length, mode):
        # Vehicle Speed (in km/h) Min = 0, Max = 255
        self.speed = speed
        self.x_position = x_position         # Vehicle Position x (in metres)
        self.y_position = y_position         # Vehicle Position y (in metres)
        self.x_steering = x_steering         # Vehicle Steering Angle (x)
        self.sensor_range = sensor_range     # Vehicle Sensor Range (in metres)
        self.width = width                   # Vehicle Width (in metres)
        self.length = length                 # Vehicle Length (in metres)
        # Vehicle must maintain this Safety Distance while driving at high speeds
        self.safety_distance_driving = 10
        self.safety_distance_stationary = 3
        self.safety_pedestrian = 20
        # Vehicle in Manual (0) or Automatic (1)
        self.mode = mode


""" Object class keeps track of the object's state """


class Object:
    def __init__(self, obj_type, speed, x_position, y_position, width, length):
        self.obj_type = obj_type
        self.speed = speed                   # Object Speed (in km/h)
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.length = length


""" Environment class that keeps track of vehicles and objects """


class Env:
    def __init__(self, v):
        self.vehicle = v
        self.objects = []
        self.object_type = ["vehicle", "person"]


""" Main Automation method """


def automation():
    # Initialize Automated Vehicle (Tabby) settings
    speed = 80
    x_position = 0
    y_position = 0
    x_steering = 0
    sensor_range = 150
    width = 2.48
    length = 4.12
    mode = 0
    tabby = Vehicle(speed, x_position, y_position,
                    x_steering, sensor_range, width, length, mode)
    environment = Env(tabby)
    running = True
    while running:
        bus = can.Bus(channel='can0', bustype='socketcan')
        bus.set_filters([
            {"can_id": 0x006, "can_mask": 0x7FF, "extended": False},
            {"can_id": 0x005, "can_mask": 0x7FF, "extended": False}
        ])
        message = bus.recv(1.0)
        try:
            if message.arbitration_id == 0x006: 
                message_dict = structure_message(message)
                print("data", message_dict['id'])
                print("data", message_dict['data'][7])
                if message_dict['data'][7] == 1:
                    environment.vehicle.mode = 1
                elif message_dict['data'][7] == 0:
                    environment.vehicle.mode = 0

            if message.arbitration_id == 0x005:
                message_dict = structure_message(message)
                print("data", message_dict['id'])
                print("data", message_dict['data'][7])
                spawn_object(environment)

        except AttributeError:
            print("No Messages Received")
            
        if environment.vehicle.mode == 1:
            check_surrounding(environment)
            hex_speed = hex(speed).lstrip("0x")
            cmd = "cansend can0 103#" + hex_speed + "00000000000001"
            os.system(cmd)


""" Check Surroundings (This will be looping) """


def check_surrounding(environment):
    # bus = can.Bus(channel='can0', bustype='socketcan')
    # bus.set_filters([
    #     {"can_id": 0x006, "can_mask": 0x7FF, "extended": False}
    # ])
    # message = bus.recv(1.0)
    # try:
    #     if message.arbitration_id == 0x006:
    #         message_dict = {
    #             'id': hex(message.arbitration_id),
    #             'data': message.data,
    #             'dlc': message.dlc
    #         }
    #         print("data", message_dict['id'])
    #         print("data", message_dict['data'][7])
    #         if message_dict['data'][7] == 1:
    #             environment.vehicle.mode = 1
    #         elif message_dict['data'][7] == 0:
    #             environment.vehicle.mode = 0
    #             return
    #
    # except AttributeError:
    #     print("No Messages Received")

    # No Object in the Environment
    if environment.objects is None:
        return

    # If Object Detected/in range, check object type
    # For vehicle
    if environment.objects[0].type == environment.object_type[0]:
        vehicle_detected(environment)
        environment.objects.clear()
        return

    # For pedestrian
    elif environment.objects[0].type == environment.object_type[1]:
        person_detected(environment)
        environment.objects.clear()
    return


""" Procedure when vehicle detected """


def vehicle_detected(environment):
    # If vehicle ahead is close and stationary or moving very slowly, apply emergencyBrakes
    if(((environment.vehicle.y_position - environment.objects[0].y_position) <
        environment.vehicle.safety_distance_driving) and
       (environment.objects[0].speed == 0 or (environment.objects[0].speed - environment.vehicle.speed > 20))):
        emergency_brakes()

    # If vehicle ahead is close and moving, adjust speed to match the vehicle ahead
    if (((environment.vehicle.y_position - environment.objects[0].y_position) <
        environment.vehicle.safety_distance_driving) and
       (environment.objects[0].speed - environment.vehicle.speed > 0)):
        for i in range(environment.vehicle.speed, environment.objects[0].speed, -1):
            environment.vehicle.speed = i
            # send canMsg with the vehicle's speed value
            hex_speed = hex(environment.vehicle.speed)
            # hex_x_position = hex(environment.vehicle.x_position)
            # hex_y_position = hex(environment.vehicle.y_position)
            # hex_object_speed = hex(environment.objects[0].speed)
            # hex_object_x_position = hex(environment.objects[0].x_position)
            cmd = "cansend can0 003#" + hex_speed + "00000000000001"
            os.system(cmd)
            # add delay if necessary
        perform_maneuver(environment)


""" Procedure when person detected """


def person_detected(environment):
    # If person is too close, apply emergencyBrakes
    if environment.vehicle.y_position - environment.objects[0].y_position < environment.vehicle.safety_pedestrian:
        emergency_brakes()

    # If person is far, apply brakes gracefully
    if environment.vehicle.y_position - environment.objects[0].y_position > environment.vehicle.safety_pedestrian:
        for i in range(environment.vehicle.speed, environment.objects[0].speed, -1):
            environment.vehicle.speed = i
    return False


""" Procedure for emergencies """


def emergency_brakes():
    # send canMsg with 100% brakes
    return False


""" Perform Maneuver when object detected ahead of the tabby """


def perform_maneuver(environment):
    switch_to_left_lane(environment)
    # for(i = environment.vehicle.speed, i < (environment.objects[0].speed + 15), i++):
    for i in range(environment.vehicle.speed, (environment.objects[0].speed + 15), 1):
        environment.vehicle.speed = i
        # send canMsg with the vehicle's speed value

    while True:
        if check_overtake(environment.vehicle, environment.objects[0]):
            break

    switch_to_right_lane(environment)


""" Switch to the left lane of the road """


def switch_to_left_lane(environment):
    while (environment.vehicle.x_position - environment.objects[0].x_position) < 1.5:
        # for(i = environment.vehicle.x_position, abs(i - environment.objects[0].x_position) > 1.5, i--):
        for i in range(abs((environment.vehicle.x_position + (environment.vehicle.width / 2)) -
                           environment.objects[0].x_position), 1, -1):
            environment.vehicle.x_position -= 1
            hex_steering = hex(100)
            cmd = "cansend can0 002#" + hex_steering + "00000000000001"
            os.system(cmd)
            # send canMsg with appropriate steering angle


""" Switch to the right lane of the road """


def switch_to_right_lane(environment):
    while (environment.vehicle.x_position - environment.objects[0].x_position) != 0:
        # for(i = environment.vehicle.x_position, abs(i - environment.objects[0].x_position) != 0, i++):
        for i in range(abs((environment.vehicle.x_position + (environment.vehicle.width / 2)) -
                           environment.objects[0].x_position) != 0, 1):
            environment.vehicle.x_position += 1
            hex_steering = hex(900)
            cmd = "cansend can0 002#" + hex_steering + "00000000000001"
            os.system(cmd)
            # send canMsg with appropriate steering angle


""" Check if the tabby has overtaken the vehicle """


def check_overtake(veh, obj):
    if (veh.y_position - obj.y_position) > veh.safety_distance_driving:
        return True
    else:
        return False


def structure_message(message):
    return {
        'id': hex(message.arbitration_id),
        'data': message.data,
        'dlc': message.dlc
    }


def spawn_object(environment):
    # Randomize Object Parameters
    object_t = random.choice("vehicle", "pedestrian")
    if object_t == environment.object_type[1]:
        object_s = 0
        object_x = environment.vehicle.x_position
        object_y = random.randrange(50, 200, 1)
        object_w = 1
        object_l = 1
    else:
        object_s = random.randrange(40, 60, 1)
        object_x = environment.vehicle.x_position
        object_y = random.randrange(100, 200, 1)
        object_w = environment.vehicle.width
        object_l = environment.vehicle.length
    obj = Object(object_t, object_s, object_x, object_y, object_w, object_l)
    environment.objects.append(obj)


if __name__ == "__main__":
    automation()
