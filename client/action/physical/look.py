import cv2
import requests
import time
from client_utils.others import wait_for_static
from adafruit_servokit import ServoKit
import numpy as np

kit = ServoKit(channels=16)

time_per_frame = 2 / 1

turn_angle_speed = 2

vertical_stand_angle = 100
vertical_up_angle = vertical_stand_angle - 60
vertical_down_angle = vertical_stand_angle + 60

horiz_stand_angle = 95
horiz_right_angle = horiz_stand_angle - 80
horiz_left_angle = horiz_stand_angle + 80


def turn_angle_horiz(src, dest):
    for angle in np.arange(src, dest, turn_angle_speed if dest > src else -turn_angle_speed):
        kit.servo[3].angle = angle
        time.sleep(0.1)


def turn_angle_vert(src, dest):
    for angle in np.arange(src, dest, turn_angle_speed if dest > src else -turn_angle_speed):
        kit.servo[1].angle = angle
        time.sleep(0.1)


def turn_neck(rad_bias):
    angle = -np.rad2deg(rad_bias) + horiz_stand_angle
    # turn_angle_horiz(kit.servo[3].angle, angle)
    kit.servo[3].angle = angle
    wait_for_static(1)


def l_up(angle=vertical_up_angle):
    # kit.servo[1].angle = vertical_stand_angle
    # turn_angle_vert(vertical_stand_angle, vertical_up_angle)
    kit.servo[1].angle = angle
    time.sleep(0.5)
    kit.servo[3].angle = horiz_stand_angle
    time.sleep(0.5)
    # kit.servo[1].angle = None
    # kit.servo[3].angle = None
    wait_for_static()


# def l_down():
#     kit.servo[1].angle = vertical_stand_angle
#     turn_angle_vert(vertical_stand_angle, vertical_down_angle)
#     kit.servo[1].angle = None

def l_left():
    # kit.servo[3].angle = horiz_stand_angle
    # turn_angle_horiz(horiz_stand_angle, horiz_left_angle)
    kit.servo[1].angle = vertical_stand_angle
    time.sleep(0.5)
    kit.servo[3].angle = horiz_left_angle
    time.sleep(0.5)
    # kit.servo[1].angle = None
    # kit.servo[3].angle = None
    wait_for_static()


def l_left_up():
    # kit.servo[3].angle = horiz_stand_angle
    # turn_angle_horiz(horiz_stand_angle, horiz_left_angle)
    # kit.servo[1].angle = vertical_stand_angle
    # turn_angle_vert(vertical_stand_angle, vertical_up_angle)
    kit.servo[1].angle = vertical_up_angle
    time.sleep(0.5)
    kit.servo[3].angle = horiz_left_angle
    time.sleep(0.5)
    # kit.servo[1].angle = None
    # kit.servo[3].angle = None
    wait_for_static()


def l_right():
    # kit.servo[3].angle = horiz_stand_angle
    # turn_angle_horiz(horiz_stand_angle, horiz_right_angle)
    kit.servo[1].angle = vertical_stand_angle
    time.sleep(0.5)
    kit.servo[3].angle = horiz_right_angle
    time.sleep(0.5)
    # kit.servo[1].angle = None
    # kit.servo[3].angle = None
    wait_for_static()


def l_right_up():
    # kit.servo[3].angle = horiz_stand_angle
    # turn_angle_horiz(horiz_stand_angle, horiz_right_angle)
    # kit.servo[1].angle = vertical_stand_angle
    # turn_angle_vert(vertical_stand_angle, vertical_up_angle)
    kit.servo[1].angle = vertical_up_angle
    time.sleep(0.5)
    kit.servo[3].angle = horiz_right_angle
    time.sleep(0.5)
    # kit.servo[1].angle = None
    # kit.servo[3].angle = None
    wait_for_static()


def l_init():
    kit.servo[1].angle = vertical_stand_angle
    time.sleep(0.5)
    kit.servo[3].angle = horiz_stand_angle
    time.sleep(0.5)
    # kit.servo[1].angle = None
    # kit.servo[3].angle = None
    wait_for_static()


def unset_motor():
    kit.servo[1].angle = None
    kit.servo[3].angle = None


def get_head_direct():
    # return {"hori_rot": kit.servo[3].angle, "vert_rot": kit.servo[1].angle}
    return kit.servo[3].angle, kit.servo[1].angle


look_funcs = {
    "look up": l_up,
    "look left": l_left,
    "look right": l_right,
    "look left up": l_left_up,
    "look right up": l_right_up,
    "look ahead": l_init,
}

if __name__ == '__main__':
    # turn_neck(0)
    # l_up()
    l_right()
    l_left()
    l_init()
    # l_up(vertical_stand_angle - 80)
