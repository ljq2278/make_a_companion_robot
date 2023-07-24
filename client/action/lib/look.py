import cv2
import requests
import time
from adafruit_servokit import ServoKit
import numpy as np

kit = ServoKit(channels=16)

time_per_frame = 2 / 1

turn_angle_speed = 5

vertical_stand_angle = 90
vertical_up_angle = 165

horiz_stand_angle = 90
horiz_right_angle = 30
horiz_left_angle = 150


def turn_angle_horiz(src, dest):
    for angle in np.arange(src, dest, turn_angle_speed if dest > src else -turn_angle_speed):
        kit.servo[3].angle = angle
        time.sleep(0.1)

def turn_angle_vert(src, dest):
    for angle in np.arange(src, dest, turn_angle_speed if dest > src else -turn_angle_speed):
        kit.servo[2].angle = angle
        time.sleep(0.1)

def l_up():
    kit.servo[1].angle = 65
    kit.servo[2].angle = vertical_stand_angle
    turn_angle_vert(vertical_stand_angle, vertical_up_angle)
    time.sleep(1)
    # turn_angle_vert(vertical_up_angle, vertical_stand_angle)
    kit.servo[2].angle = None
    kit.servo[1].angle = None


def l_left():
    kit.servo[3].angle = horiz_stand_angle
    turn_angle_horiz(horiz_stand_angle, horiz_left_angle)
    time.sleep(1)
    # turn_angle_horiz(horiz_left_angle, horiz_stand_angle)
    kit.servo[3].angle = None

def l_right():
    kit.servo[3].angle = horiz_stand_angle
    turn_angle_horiz(horiz_stand_angle, horiz_right_angle)
    time.sleep(1)
    # turn_angle_horiz(horiz_right_angle, horiz_stand_angle)
    kit.servo[3].angle = None

def l_init():
    kit.servo[1].angle = 65
    kit.servo[2].angle = 90
    kit.servo[3].angle = 90
    time.sleep(1)
    kit.servo[1].angle = None
    kit.servo[2].angle = None
    kit.servo[3].angle = None

if __name__ == '__main__':
    l_right()