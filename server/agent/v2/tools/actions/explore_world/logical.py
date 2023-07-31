import time

import requests
from server_utils.path import CLIENT_ACTION_IP_PATH
from server_utils.others import parse_txt_and_mood, wait_for_human_response
from inputs.vision.api import get_objs
from inputs.keyboard.api import get_keyboard_input
import numpy as np


def do_explore_async(second_tm):
    start_tm = int(time.time())
    response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "look ahead"})
    if response.text == "true" and "Person" in get_objs():
        return True
    response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "look left"})
    if response.text == "true" and "Person" in get_objs():
        return True
    response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "look left up"})
    if response.text == "true" and "Person" in get_objs():
        return True
    response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "look up"})
    if response.text == "true" and "Person" in get_objs():
        return True
    response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "look right up"})
    if response.text == "true" and "Person" in get_objs():
        return True
    response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "look right"})
    if response.text == "true" and "Person" in get_objs():
        return True
    return False


def do_query(query):
    query_parsed = parse_txt_and_mood(query)
    response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "show_mood#" + query_parsed["mood"]})
    if response.text != "true":
        print("show mood failed! \n")
    response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "say#" + query_parsed["speech"]})
    if response.text == "true":
        wait_for_human_response()
        return get_keyboard_input()
    else:
        return "the greeting send failed ..."
