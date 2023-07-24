import cv2
import requests
import time
from lib.move import t_stop, t_up, t_down, t_right, t_left
import numpy as np

# Set the server URL (adjust the IP address and port if needed)
SERVER_URL = "http://192.168.1.9:8005/move/"

param_direct = {"forward", "backward", "left", "right"}
param_dist = {"0", "1", "3", "6"}
speed = 50


def act_and_send_complete(param):
    param_ls = param.strip().split("_")
    if len(param_ls) != 2:
        return ""
    if param_ls[0] in param_direct and param_ls[1] in param_dist:
        if param_ls[0] == "backward":
            t_down(speed, int(param_ls[1]))
        elif param_ls[0] == "left":
            t_left(speed, int(param_ls[1]))
        elif param_ls[0] == "right":
            t_right(speed, int(param_ls[1]))
        else:
            t_up(speed, int(param_ls[1]))
        send_comp_and_get_action(complete="true")
        return ""
    else:
        print("invalid param: ", param)
        return ""


def send_comp_and_get_action(complete="false"):
    print('send comp ...')
    response = requests.post(SERVER_URL, data={'complete': complete})
    if response.status_code == 200:
        action = response.json()["action"]
        print('get action: ', action)
        return action
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ""


if __name__ == "__main__":
    recv_order = ""
    while True:
        if recv_order == "":
            # get action here
            recv_order = send_comp_and_get_action()
        else:
            # act and send result here
            recv_order = act_and_send_complete(recv_order)
        time.sleep(0.5)
