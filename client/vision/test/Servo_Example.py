# #!/usr/bin/python
#
# from Adafruit_PWM_Servo_Driver import PWM
# import time
#
# # ===========================================================================
# # Example Code
# # ===========================================================================
#
# # Initialise the PWM device using the default address
# pwm = PWM(0x40)
# # Note if you'd like more debug output you can instead run:
# #pwm = PWM(0x40, debug=True)
#
# servoMin = 130  # Min pulse length out of 4096  #150
# servoMax = 620  # Max pulse length out of 4096 #600
#
# def setServoPulse(channel, pulse):
#   pulseLength = 1000000                   # 1,000,000 us per second
#   pulseLength /= 60                       # 60 Hz
#   print "%d us per period" % pulseLength
#   pulseLength /= 4096                     # 12 bits of resolution
#   print "%d us per bit" % pulseLength
#   pulse *= 1000
#   pulse /= pulseLength
#   pwm.setPWM(channel, 0, pulse)
#
# pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
# while (True):
#   # Change speed of continuous servo on channel O
#   pwm.setPWM(0,0,servoMin)
#   pwm.setPWM(1,0,servoMin)
#   pwm.setPWM(2,0,servoMin)
#   pwm.setPWM(3,0,servoMin)
#   pwm.setPWM(4,0,servoMin)
#   pwm.setPWM(5,0,servoMin)
#   pwm.setPWM(6,0,servoMin)
#   pwm.setPWM(7,0,servoMin)
#   pwm.setPWM(8,0,servoMin)
#   pwm.setPWM(9,0,servoMin)
#   pwm.setPWM(10,0,servoMin)
#   pwm.setPWM(11,0,servoMin)
#   pwm.setPWM(12,0,servoMin)
#   pwm.setPWM(13,0,servoMin)
#   pwm.setPWM(14,0,servoMin)
#   pwm.setPWM(15,0,servoMin)
#   time.sleep(3)
#   pwm.setPWM(0,0,servoMax)
#   pwm.setPWM(1,0,servoMax)
#   pwm.setPWM(2,0,servoMax)
#   pwm.setPWM(3,0,servoMax)
#   pwm.setPWM(4,0,servoMax)
#   pwm.setPWM(5,0,servoMax)
#   pwm.setPWM(6,0,servoMax)
#   pwm.setPWM(7,0,servoMax)
#   pwm.setPWM(8,0,servoMax)
#   pwm.setPWM(9,0,servoMax)
#   pwm.setPWM(10,0,servoMax)
#   pwm.setPWM(11,0,servoMax)
#   pwm.setPWM(12,0,servoMax)
#   pwm.setPWM(13,0,servoMax)
#   pwm.setPWM(14,0,servoMax)
#   pwm.setPWM(15,0,servoMax)
#   time.sleep(3)
#
#
#
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for a standard servo on channel 0 and a continuous rotation servo on channel 1."""
import time
from adafruit_servokit import ServoKit
import numpy as np

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
# kit.frequency = 100
# kit.servo[0].angle = 90
# kit.servo[1].angle = 90
# kit.servo[2].angle = 90
# kit.servo[3].angle = 90
kit.servo[0].angle = None
kit.servo[1].angle = None
kit.servo[2].angle = None


if kit.servo[3].angle is None:
  kit.servo[3].angle = 90
start_angle = kit.servo[3].angle
dest_angle = 130
speed = 2
for angle in np.arange(start_angle, dest_angle, speed if dest_angle > start_angle else -speed):
    kit.servo[3].angle = angle
    time.sleep(0.1)
kit.servo[3].angle = None