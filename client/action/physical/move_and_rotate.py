import RPi.GPIO as GPIO
import time

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


def m_up(mv_tm, mv_speed=20):
    motor_speed = mv_speed_to_motor(mv_speed)
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1
    time.sleep(mv_tm)
    _stop()


def m_down(mv_tm, mv_speed=20):
    motor_speed = mv_speed_to_motor(mv_speed)
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1
    time.sleep(mv_tm)
    _stop()


def r_left(rot_tm, rot_speed=90):
    motor_speed = rot_speed_to_motor(rot_speed)
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1
    time.sleep(rot_tm)
    _stop()


def r_right(rot_tm, rot_speed=90):
    motor_speed = rot_speed_to_motor(rot_speed)
    L_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(motor_speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1
    time.sleep(rot_tm)
    _stop()


if __name__ == '__main__':
    try:
        # m_up(10, 20)
        # m_down(5, 20)
        r_left(0.5)
        # t_right(50, 3)
        # _stop()
        # time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()
