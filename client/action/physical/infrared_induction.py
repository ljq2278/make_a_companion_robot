import RPi.GPIO as GPIO
import numpy as np
import time

data_port = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(data_port, GPIO.IN)


def check_people_near():
    # return np.mean([float(GPIO.input(data_port)) for _ in range(0, 10)])
    signals = []
    for i in range(0, 20):
        signals.append(GPIO.input(data_port))
        time.sleep(0.1)
    return False if np.mean(signals) == 0.0 else True


if __name__ == '__main__':
    while True:
        # GPIO.setup(data_port, GPIO.IN)
        print(check_people_near())
        # GPIO.cleanup(data_port)
