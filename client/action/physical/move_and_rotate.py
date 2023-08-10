import RPi.GPIO as GPIO
import time
from action.physical.compass import get_body_direct
import action.physical.laser as laser
import action.physical.ultrasound_measure as us

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
default_rot_speed = 90

def motor_to_mv_speed(motor_speed):
    return 17.225 / 50 * motor_speed


def motor_to_rot_speed(motor_speed):
    return 90 / 62 * motor_speed


def mv_speed_to_motor(mv_speed):
    return 50 / 17.225 * mv_speed


def rot_speed_to_motor(rot_speed):
    return 50 / 90 * rot_speed


def _stop():
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, False)  # BIN1


def m_up(mv_tm, mv_speed=default_mv_speed):
    mv_tm = min(laser.get_dist() - 10, mv_tm * mv_speed) / mv_speed
    motor_speed = mv_speed_to_motor(mv_speed)
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1
    time.sleep(mv_tm)
    _stop()


def m_down(mv_tm, mv_speed=default_mv_speed):
    mv_tm = min(us.get_dist() - 10, mv_tm * mv_speed) / mv_speed
    motor_speed = mv_speed_to_motor(mv_speed)
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1
    time.sleep(mv_tm)
    _stop()


def r_left(rot_tm, rot_speed=default_rot_speed):
    motor_speed = rot_speed_to_motor(rot_speed)
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1
    time.sleep(rot_tm)
    _stop()


def r_right(rot_tm, rot_speed=default_rot_speed):
    motor_speed = rot_speed_to_motor(rot_speed)
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1
    time.sleep(rot_tm)
    _stop()


def rotate_to_dest_rad(dest_rad):
    cur_rad = get_body_direct(use_rad=True)
    while abs(cur_rad - dest_rad) > 0.1:
        print("cur_rad: ", cur_rad)
        if dest_rad - cur_rad > 0:
            r_right(0.1)
        else:
            r_left(0.1)
        cur_rad = get_body_direct(use_rad=True)


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
        rotate_to_dest_rad(-2.925)
    except KeyboardInterrupt:
        GPIO.cleanup()
