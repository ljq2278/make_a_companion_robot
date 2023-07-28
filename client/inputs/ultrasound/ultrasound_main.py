import cv2
import requests
import time
import numpy as np
from lib.check_obstacle import ur_disMeasure
from formats.states_format import Obstacle
import json

# Set the server URL (adjust the IP address and port if needed)
SERVER_URL = "http://192.168.1.9:8006/ultrasound/"


def send_data():
    dist = ur_disMeasure()
    obstacle = Obstacle(dist=str(int(dist)) + "cm")
    obstacle_obj = vars(obstacle)
    print('send data ... ', obstacle_obj)
    response = requests.post(SERVER_URL, json=obstacle_obj)
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
