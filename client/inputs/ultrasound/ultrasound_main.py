import cv2
import requests
import time
import numpy as np
from action.physical.ultrasound_measure import get_dist
from client_utils.path import ULTRASOUND_SERVER_IP_PATH
from formats.states_format import Obstacle
import json


def send_data():
    dist = get_dist()
    obstacle = Obstacle(dist=str(int(dist)) + "cm")
    obstacle_dict = vars(obstacle)
    print('send data ... ', obstacle_dict)
    response = requests.post(ULTRASOUND_SERVER_IP_PATH, json=obstacle_dict)
    print('Response:', response.status_code, response.text)


if __name__ == "__main__":
    # Change the '0' to the appropriate camera ID if needed
    recv_order = ""
    while True:
        try:
            time.sleep(0.5)
            send_data()
        except Exception as e:
            print(e)
