import cv2
import requests
import time
import numpy as np
from client_utils.path import BODY_SERVER_IP_PATH
from action.physical.look import get_direct
from formats.states_format import Body



def send_data():
    direct = get_direct()
    body = Body(hori_rot=direct["hori_rot"], vert_rot=direct["vert_rot"])
    body_dict = vars(body)
    print('send data ... ', body_dict)
    response = requests.post(BODY_SERVER_IP_PATH, json=body_dict)
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
