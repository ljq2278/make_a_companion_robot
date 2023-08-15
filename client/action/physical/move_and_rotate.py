# notice the power saving!

import RPi.GPIO as GPIO
import time
from action.physical.compass import get_body_direct
from action.physical.posture import get_posture
import action.physical.laser as laser
from action.physical.photic import get_photic
import action.physical.ultrasound_measure as us
import numpy as np

PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)

GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 100)
L_Motor.start(0)

R_Motor = GPIO.PWM(PWMB, 100)
R_Motor.start(0)

default_mv_speed = 20
default_rot_speed = 60

m_unit_tm = 0.5
r_unit_tm = 0.1

max_rot_unit_conts = 36
# stop_accelerate = -5
# stop_x_gravity = 4
# stop_abs_accelerate = 5
# stop_abs_gyro = 0.5
stop_abs_accelerate = 4
stop_abs_gyro = 0.3


def motor_to_mv_speed(motor_speed):
    return 17.225 / 50 * motor_speed


def motor_to_rot_speed(motor_speed):
    return 90 / 62 * motor_speed


def mv_speed_to_motor(mv_speed):
    return 50 / 17.225 * mv_speed


def rot_speed_to_motor(rot_speed):
    return 50 / 90 * rot_speed

def _start_motors():
    L_Motor.start(0)
    R_Motor.start(0)

def _stop_motors():
    L_Motor.stop()
    R_Motor.stop()

def _set_motors_m_up(motor_speed):
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1

def _set_motors_m_down(motor_speed):
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1

def _set_motors_r_left(motor_speed):
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1

def _set_motors_r_right(motor_speed):
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1

def _stop():
    print("_stop")
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, False)  # BIN1


def _photic_condition():
    _stop_motors()
    if laser.get_dist() < 10:
        _start_motors()
        return False
    if get_photic() > 11:
        _start_motors()
        return False
    _start_motors()
    return True


def _m_unit():
    time.sleep(m_unit_tm)
    _stop_motors()
    gx, gy, gz, ax, ay, az = get_posture()
    _start_motors()
    # if ax < stop_accelerate or ax > stop_x_gravity:
    if np.abs(ax) > stop_abs_accelerate:
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s, Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (gx, gy, gz, ax, ay, az))
        return False
    else:
        print("ax: ", ax)
        return True


def _r_unit():
    time.sleep(r_unit_tm)
    _stop_motors()
    gx, gy, gz, ax, ay, az = get_posture()
    _start_motors()
    # if ax < stop_accelerate or ax > stop_x_gravity:
    if np.abs(gx) > stop_abs_gyro:
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s, Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (gx, gy, gz, ax, ay, az))
        return False
    else:
        print("gx: ", gx)
        return True


def m_up_photic(mv_tm, mv_speed=default_mv_speed):
    # mv_tm = min(laser.get_dist() - 10, mv_tm * mv_speed) / mv_speed
    motor_speed = mv_speed_to_motor(mv_speed)
    _set_motors_m_up(motor_speed)
    mv_success = photic_success = True
    cont = 0
    while mv_success and photic_success and cont * m_unit_tm < mv_tm:
        print("m_up_photic unit")
        mv_success = _m_unit()
        print("_photic_condition")
        photic_success = _photic_condition()
        _set_motors_m_up(motor_speed)
        cont += 1
    success = mv_success and photic_success
    if not success:
        m_down(3, 10)
    _stop()
    return success


def m_up(mv_tm, mv_speed=default_mv_speed):
    # mv_tm = min(laser.get_dist() - 10, mv_tm * mv_speed) / mv_speed
    motor_speed = mv_speed_to_motor(mv_speed)
    _set_motors_m_up(motor_speed)
    success = True
    cont = 0
    while success and cont * m_unit_tm < mv_tm:
        success = _m_unit()
        _set_motors_m_up(motor_speed)
        cont += 1
    _stop()
    return success


def m_down(mv_tm, mv_speed=default_mv_speed):
    # mv_tm = min(laser.get_dist() - 10, mv_tm * mv_speed) / mv_speed
    motor_speed = mv_speed_to_motor(mv_speed)
    _set_motors_m_down(motor_speed)
    success = True
    cont = 0
    while success and cont * m_unit_tm < mv_tm:
        success = _m_unit()
        _set_motors_m_down(motor_speed)
        cont += 1
    _stop()
    return success


def r_left(rot_tm, rot_speed=default_rot_speed):
    motor_speed = rot_speed_to_motor(rot_speed)
    _set_motors_r_left(motor_speed)
    success = True
    cont = 0
    while success and cont * r_unit_tm < rot_tm:
        print("r_left_r_unit")
        success = _r_unit()
        _set_motors_r_left(motor_speed)
        cont += 1
    _stop()
    return success


def r_right(rot_tm, rot_speed=default_rot_speed):
    motor_speed = rot_speed_to_motor(rot_speed)
    _set_motors_r_right(motor_speed)
    success = True
    cont = 0
    while success and cont * r_unit_tm < rot_tm:
        print("r_right_r_unit")
        success = _r_unit()
        _set_motors_r_right(motor_speed)
        cont += 1
    _stop()
    return success


def rotate_to_dest_rad(dest_rad, rot_speed=default_rot_speed):
    cur_rad = get_body_direct(use_rad=True)
    success = True
    cont = 0
    while success and abs(cur_rad - dest_rad) > 0.1 and cont < max_rot_unit_conts:
        cont += 1
        # print("cur_rad: ", cur_rad)
        if dest_rad - cur_rad > 0:
            print("rotate right")
            success = r_right(0.1, rot_speed)
        else:
            print("rotate left")
            success = r_left(0.1, rot_speed)
        cur_rad = get_body_direct(use_rad=True)
    if not success:
        print("rotate stuck!")
    else:
        print("rotate success!")


def go_wander():
    flg = 1
    while True:
        rotate_to_dest_rad(np.random.random() * np.pi * 2 - np.pi)
        if flg == 1:
            print("go up start")
            success = m_up(5)
            print("go up end")
        else:
            print("go down start")
            success = m_down(5)
            print("go down end")
        # if not success:
        #     time.sleep(2)
        #     flg = 1 - flg
        flg = 1 - flg


move_funcs = {
    "up": m_up,
    "back": m_down,
    "rotate": rotate_to_dest_rad,
}

if __name__ == '__main__':
    try:
        # m_up(0.5, 10)
        # m_down(5, 20)
        # r_left(0.5)
        # t_right(50, 3)
        # _stop()
        # time.sleep(2)
        # rotate_to_dest_rad(-2.925)
        # m_up2(10)
        # m_down2(10)
        go_wander()
        # rotate_to_dest_rad2(0)
    except KeyboardInterrupt:
        GPIO.cleanup()
