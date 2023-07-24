import json
import requests
import time
from lib.move_and_rotate import m_up, m_down, r_left, r_right
# from lib.rotate import r_left, r_right
from lib.look import l_left, l_right, l_up, l_init
import numpy as np

# Set the server URL (adjust the IP address and port if needed)
SERVER_URL = "http://192.168.1.9:8005/action/"
action_set = {"move", "look"}
direct_set = {"forward", "left", "right", "half_left", "half_right", "backward"}
angle_set = {}  # 0~2
dist_set = {}  # 0~5
speed = 50
recv_order = ""
state = "waiting_order"


def init_actions():
    l_init()


def get_order_and_act():
    global recv_order, state
    if recv_order != "":
        order_dict = json.loads(recv_order, encoding='utf-8')
        if order_dict["action"] == "move":
            if order_dict["direct"] == "backward":
                m_down(speed, int(float(order_dict["dist"])))
            elif order_dict["direct"] == "forward":
                m_up(speed, int(float(order_dict["dist"])))
        elif order_dict["action"] == "rotate":
            if order_dict["direct"] == "left":
                r_left(speed, int(float(order_dict["angle"])))
            elif order_dict["direct"] == "right":
                r_right(speed, int(float(order_dict["angle"])))
        elif order_dict["action"] == "look":
            if order_dict["direct"] == "left":
                l_left()
            elif order_dict["direct"] == "right":
                l_right()
            elif order_dict["direct"] == "up":
                l_up()
        recv_order = ""
        state = "complete"
    else:
        state = "waiting_order"
    send_state_and_get_action()


def send_state_and_get_action():
    global recv_order
    print('send comp ...')
    response = requests.post(SERVER_URL, data={'state': state})
    if response.status_code == 200:
        recv_order = response.json()["action"]
        print('get action: ', recv_order)
    else:
        print(f"Error: {response.status_code} - {response.text}")


if __name__ == "__main__":
    while True:
        try:
            init_actions()
            time.sleep(1)
            get_order_and_act()
        except Exception as e:
            print(e)
