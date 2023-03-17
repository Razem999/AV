"""
We got the game from Youtube, Python Simplified:
https://www.youtube.com/watch?v=W-QOtdD3qx4&t=59s

We got the car.png from:
https://stackoverflow.com/questions/62240557/how-could-i-make-a-basic-car-physics-in-pygame
"""

import pygame
from pygame.locals import *
import can
import math
import random
import os


# shape parameters
width = 200
height = 500
size = (width, height)
road_w = int(width/2)

# road parameters
right_lane = width/2 + road_w/2
left_lane = width/2 - road_w/2
screen = pygame.display.set_mode(size)

# set window title
pygame.display.set_caption("Simulation Car")
bg = pygame.image.load("Images/Road.png")
tiles = math.ceil(height / bg.get_height()) + 1


""" Vehicle class keeps track of the vehicle's state """


class Vehicle:
    def __init__(self, actual_speed, car, rect):
        # Vehicle Speed (in km/h) Min = 0, Max = 255
        self.actual_speed = actual_speed
        self.game_speed = round(self.actual_speed * 0.1)
        self.speed = self.game_speed
        self.car = car
        self.rect = rect
        # Vehicle must maintain this Safety Distance while driving at high speeds
        self.safety_distance_driving = 200
        self.safety_distance_stationary = 100
        self.safety_pedestrian = 50
        # Vehicle in Manual (0) or Automatic (1)
        # self.mode = mode


""" Object class keeps track of the object's state """


class Object:
    def __init__(self, obj_type, actual_speed, obj, rect):
        self.obj_type = obj_type
        self.actual_speed = actual_speed
        self.game_speed = round(self.actual_speed * 0.1)
        self.speed = self.game_speed                 # Object Speed (in km/h)
        self.obj = obj
        self.rect = rect


""" Environment class that keeps track of vehicles and objects """


class Env:
    def __init__(self, v):
        self.vehicle = v
        self.objects = []
        self.object_type = ["vehicle", "pedestrian"]


def game():
    temp = True

    # initiallize the app
    pygame.init()
    running = True

    # set window size
    clock = pygame.time.Clock()

    tab = tabby()
    environment = Env(tab)

    # game loop
    while running:
        # bus = can.Bus(channel='can0', bustype='socketcan')
        # bus.set_filters([
        #     {"can_id": 0x006, "can_mask": 0x7FF, "extended": False},
        #     {"can_id": 0x005, "can_mask": 0x7FF, "extended": False}
        # ])
        # message = bus.recv(1.0)
        # try:
        #     if message.arbitration_id == 0x006:
        #         message_dict = structure_message(message)
        #         print("data", message_dict['id'])
        #         print("data", message_dict['data'][7])
        #         if message_dict['data'][7] == 1:
        #             environment.vehicle.mode = 1
        #         elif message_dict['data'][7] == 0:
        #             environment.vehicle.mode = 0
        #
        #     if message.arbitration_id == 0x005:
        #         obj = spawn_object()
        #         environment.objects.append(obj)
        #
        # except AttributeError:
        #     print("No Messages Received")
        print("START")
        clock.tick(50)

        """ IMAGE TESTING """
        # Appending the image to the back of the same image
        i = 0
        while i < tiles:
            screen.blit(bg, (0, -4200 * i + tab.speed))
            i += 1

        # Frame for scrolling
        tab.speed += tab.game_speed
        # tab.speed += 5

        # Reset the scroll frame
        if abs(tab.speed) > bg.get_height() - 750:
            tab.speed = 0

        # Closing the frame of scrolling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        """ IMAGE TESTING END """

        # animate enemy vehicle
        if temp:
            obj = spawn_object(environment)
            environment.objects.append(obj)
            update_display(environment)

        print("MIDDLE")
        temp = False
        update_display(environment)

        if environment.objects:
            vehicle_behaviour(environment)
            if environment.objects[0].obj_type == environment.object_type[0]:
                vehicle_detected(environment)
            elif environment.objects[0].obj_type == environment.object_type[1]:
                pedestrian_detected(environment)

        # place car images on the screen
        update_display(environment)
        print("END")


def tabby():
    # load player vehicle
    car = pygame.image.load("Images/car.png")
    # resize image
    car = pygame.transform.scale(car, (100, 100))
    car_loc = car.get_rect()
    car_loc.center = right_lane, height * 0.8
    tabby_speed = 80
    return Vehicle(tabby_speed, car, car_loc)


def spawn_object(environment):
    object_type = ["vehicle", "pedestrian"]
    object_t = random.choice(object_type)
    if object_t == object_type[0]:
        obj = pygame.image.load("Images/car1.png")
        obj = pygame.transform.scale(obj, (100, 100))
        obj_loc = obj.get_rect()
        obj_loc.center = right_lane, environment.vehicle.rect[1] - (random.randrange(500, 1000, 1))
        speed = round(random.randrange(50, 70))
        print(speed)
    else:
        obj = pygame.image.load("Images/Pedestrian.png")
        obj = pygame.transform.scale(obj, (20, 50))
        obj_loc = obj.get_rect()
        obj_loc.center = right_lane, environment.vehicle.rect[1] - (random.randrange(800, 1400, 1))
        speed = 30
    return Object(object_t, speed, obj, obj_loc)


def vehicle_behaviour(environment):
    environment.objects[0].rect[1] += environment.objects[0].speed

    if environment.objects[0].rect[1] > height:
        environment.objects.pop(0)
        switch_to_right_lane(environment)


def vehicle_detected(environment):
    # If vehicle ahead is close and stationary or moving very slowly, apply emergencyBrakes
    if(((environment.vehicle.rect[1] - environment.objects[0].rect[1]) <
        environment.vehicle.safety_distance_driving - 30) and
       (environment.objects[0].speed == 0 or (environment.objects[0].speed - environment.vehicle.speed > 5))):
        emergency_brakes(environment)

    print("Tabby = ", environment.vehicle.game_speed)
    print("Vehicle = ", environment.objects[0].game_speed)
    print((environment.vehicle.rect[1] - environment.objects[0].rect[1]))
    # If vehicle ahead is close and moving, adjust speed to match the vehicle ahead
    if (((environment.vehicle.rect[1] - environment.objects[0].rect[1]) <
        environment.vehicle.safety_distance_driving) and
       (environment.vehicle.actual_speed - environment.objects[0].speed > 0)):
        while environment.objects[0].speed != 0:
            environment.objects[0].speed -= 1
            environment.vehicle.game_speed -= 1
            print(environment.objects[0].speed)
            update_display(environment)
            # send canMsg with the vehicle's speed value
            hex_speed = hex(environment.vehicle.actual_speed)
            cmd = "cansend can0 003#" + hex_speed + "00000000000001"
            # os.system(cmd)
        perform_maneuver(environment)


def pedestrian_detected(environment):
    print("ped 1")
    # If person is too close, apply emergencyBrakes
    print(environment.vehicle.rect[1])
    print(environment.objects[0].rect[1])
    if environment.vehicle.rect[1] - environment.objects[0].rect[1] < environment.vehicle.safety_pedestrian:
        print("ped 2")
        emergency_brakes(environment)
        update_display(environment)

    # If person is far, apply brakes gracefully
    if environment.vehicle.rect[1] - environment.objects[0].rect[1] < environment.vehicle.safety_distance_stationary:
        while environment.vehicle.game_speed != 0:
            environment.vehicle.game_speed -= 1
            update_display(environment)
            print("ped 3")
        environment.objects[0].speed = 0
        delay(1000, environment)
        environment.objects.pop(0)
        environment.vehicle.game_speed = 8


def perform_maneuver(environment):
    switch_to_left_lane(environment)
    temp = environment.vehicle.game_speed
    while environment.vehicle.game_speed < temp + 5:
        environment.vehicle.game_speed += 1
        environment.objects[0].speed += 1
        # send canMsg with the vehicle's speed value

    # while True:
    #     update_display(environment)
    #     if check_overtake(environment.vehicle, environment.objects[0]):
    #         break

    # switch_to_right_lane(environment)


""" Switch to the left lane of the road """


def switch_to_left_lane(environment):
    print("Go Left")
    print((environment.vehicle.rect[0] - environment.objects[0].rect[0]))
    print(environment.vehicle.rect[0])
    while (environment.vehicle.rect[0] - environment.objects[0].rect[0]) > -100:
        environment.vehicle.rect[0] -= 1
        update_display(environment)
        print(environment.vehicle.rect[0])
        # for(i = environment.vehicle.x_position, abs(i - environment.objects[0].x_position) > 1.5, i--):
        # for i in range(int(abs((environment.vehicle.rect[0] + (environment.vehicle.rect[2] / 2)) -
        #                    environment.objects[0].rect[0])), 1, -1):
        #     environment.vehicle.rect[0] -= 1
        hex_steering = hex(100)
        cmd = "cansend can0 102#" + hex_steering + "00000000000001"
        # os.system(cmd)
        # send canMsg with appropriate steering angle


""" Switch to the right lane of the road """


def switch_to_right_lane(environment):
    while (environment.vehicle.rect[0] - environment.objects[0].rect[0]) < -20:
        environment.vehicle.rect[0] += 1
        print(environment.vehicle.rect[0])
        update_display(environment)
        hex_steering = hex(900)
        cmd = "cansend can0 102#" + hex_steering + "00000000000001"
        # os.system(cmd)
    environment.vehicle.game_speed = 8
        # send canMsg with appropriate steering angle


""" Check if the tabby has overtaken the vehicle """


def check_overtake(veh, obj):
    if (veh.rect[1] - obj.rect[1]) > veh.safety_distance_driving:
        return True
    else:
        return False


def emergency_brakes(environment):
    while environment.vehicle.speed != 0:
        environment.vehicle.game_speed = environment.vehicle.speed - (environment.vehicle.speed * 0.02)
        environment.objects[0].speed = environment.vehicle.speed
        update_display(environment)
        # send canMsg with 100% brakes
        hex_brakes = hex(20)
        cmd = "cansend can0 101#" + hex_brakes + "00000000000001"
        # os.system(cmd)
    return


def structure_message(message):
    return {
        'id': hex(message.arbitration_id),
        'data': message.data,
        'dlc': message.dlc
    }


def delay(time, environment):
    i = 0
    while i < time:
        i += 1
        print(i)
        update_display(environment)


def update_display(environment):
    screen.blit(environment.objects[0].obj, environment.objects[0].rect)
    screen.blit(environment.vehicle.car, environment.vehicle.rect)
    pygame.display.update()


if __name__ == "__main__":
    game()
    pygame.quit()
    quit()
