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


""" Vehicle class keeps track of the vehicle's state """


class Vehicle:
    def __init__(self, speed, car, rect):
        # Vehicle Speed (in km/h) Min = 0, Max = 255
        self.speed = speed
        self.car = car
        self.rect = rect
        # Vehicle must maintain this Safety Distance while driving at high speeds
        self.safety_distance_driving = 10
        self.safety_distance_stationary = 3
        self.safety_pedestrian = 20
        # Vehicle in Manual (0) or Automatic (1)
        # self.mode = mode


""" Object class keeps track of the object's state """


class Object:
    def __init__(self, obj_type, speed, car, rect):
        self.obj_type = obj_type
        self.speed = speed                   # Object Speed (in km/h)
        self.car = car
        self.rect = rect


""" Environment class that keeps track of vehicles and objects """


class Env:
    def __init__(self, v):
        self.vehicle = v
        self.objects = []
        self.object_type = ["vehicle", "person"]


def game():
    # shape parameters
    width = 200
    height = 500
    size = (width, height)
    road_w = int(width/2)

    # # location parameters
    # right_lane = width/2 + road_w/4
    # left_lane = width/2 - road_w/4

    right_lane = width/2 + road_w/2
    left_lane = width/2 - road_w/2

    # animation parameters
    speed = 10

    # initiallize the app
    pygame.init()
    running = True

    # set window size
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    # set window title
    pygame.display.set_caption("Simulation Car")
    bg = pygame.image.load("Images/Road.png")

    tiles = math.ceil(height / bg.get_height()) + 1

    tab = tabby(right_lane, height)
    environment = Env(tab)

    counter = 0
    # game loop
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

        clock.tick(50)
        counter += 1

        """ IMAGE TESTING """
        # Appending the image to the back of the same image
        i = 0
        while i < tiles:
            screen.blit(bg, (0, -4200 * i + tab.speed))
            i += 1

        # Frame for scrolling
        tab.speed += 1

        # Reset the scroll frame
        if abs(tab.speed) > bg.get_height() - 750:
            tab.speed = 0

        # Closing the frame of scrolling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        """ IMAGE TESTING END """

        # animate enemy vehicle
        if ()
        obj = vehicle(right_lane, height)
        # environment.objects.append(veh)
        obj.rect[1] += 10
        # environment.objects[0].rect[1] += 10
        # car2_loc[1] += 2
        # if car2_loc[1] > height:
        # if environment.objects[0].rect[1] > height:
        if obj.rect[1] > height:
            # randomly select lane
            if random.randint(0, 1) == 0:
                # car2_loc.center = right_lane, -200
                obj.rect.center = right_lane, -200
            else:
                # car2_loc.center = left_lane, -200
                obj.rect.center = left_lane, -200
            # car2_loc.center = right_lane, -200
            # veh.rect.center = right_lane, -200

        # place car images on the screen
        # screen.blit(car, car_loc)
        screen.blit(tab.car, tab.rect)
        # screen.blit(car2, car2_loc)
        screen.blit(obj.car, obj.rect)
        # apply changes
        pygame.display.update()

# collapse application window
# pygame.quit()


def tabby(right_lane, height):
    # load player vehicle
    car = pygame.image.load("Images/car.png")
    # resize image
    car = pygame.transform.scale(car, (100, 100))
    car_loc = car.get_rect()
    car_loc.center = right_lane, height * 0.8
    tabby_speed = 0
    return Vehicle(tabby_speed, car, car_loc)


def vehicle(right_lane, height):
    # load player vehicle
    car = pygame.image.load("Images/car1.png")
    # resize image
    car = pygame.transform.scale(car, (100, 100))
    car_loc = car.get_rect()
    car_loc.center = right_lane, height * 0.2
    object_type = ["vehicle", "pedestrian"]
    object_t = random.choice(object_type)
    vehicle_speed = 10
    return Object(object_t, vehicle_speed, car, car_loc)


if __name__ == "__main__":
    game()
    pygame.quit()
    quit()
