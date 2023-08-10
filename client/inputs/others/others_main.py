import sys
sys.path.append(r'/home/pi/Code/client')

import requests
from action.physical.laser import get_dist
from action.physical.voltage import get_voltage
from action.physical.look import get_head_direct
from action.physical.compass import get_body_direct
from action.physical.infrared_induction import check_people_near
from client_utils.path import OTHERS_SERVER_IP_PATH
from client_utils.others import get_task_state
from formats.states_format import Others


def send_data():
    body_direct = get_body_direct()
    head_hori, head_vert = get_head_direct()
    up_dist = get_dist()
    voltage = get_voltage()
    person_near = check_people_near()  # take 2 seconds
    last_async_task_info = get_task_state()
    others = Others(up_dist=int(up_dist),
                    voltage=voltage,
                    person_near=person_near,
                    head_hori=int(head_hori),
                    head_vert=int(head_vert),
                    body_direct=int(body_direct),
                    last_async_task=last_async_task_info["last_async_task"],
                    last_async_task_state=last_async_task_info["last_async_task_state"],
                    last_async_task_result=last_async_task_info["last_async_task_result"]
                    )
    others_dict = vars(others)
    print('send data ... ', others_dict)
    response = requests.post(OTHERS_SERVER_IP_PATH, json=others_dict)
    print('Response:', response.status_code, response.text)


if __name__ == "__main__":
    # Change the '0' to the appropriate camera ID if needed
    recv_order = ""
    while True:
        try:
            send_data()
        except Exception as e:
            print(e)
