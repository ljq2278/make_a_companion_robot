import cv2
import requests
import time
import numpy as np
from action.physical.voltage import get_voltage
from client_utils.path import KERNEL_SERVER_IP_PATH
from formats.states_format import Kernel
import json

def send_data():
    voltage = get_voltage()
    kernel = Kernel(voltage=str(int(voltage)))
    kernel_dict = vars(kernel)
    print('send data ... ', kernel_dict)
    response = requests.post(KERNEL_SERVER_IP_PATH, json=kernel_dict)
    print('Response:', response.status_code, response.text)


if __name__ == "__main__":
    # Change the '0' to the appropriate camera ID if needed
    recv_order = ""
    while True:
        try:
            # time.sleep(0.5)
            send_data()
        except Exception as e:
            print(e)