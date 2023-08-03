import requests

from action.physical.ultrasound_measure import get_dist
from action.physical.voltage import get_voltage
from action.physical.infrared_induction import check_people_near
from client_utils.path import OTHERS_SERVER_IP_PATH
from formats.states_format import Others


def send_data():
    us_dist = get_dist()
    voltage = get_voltage()
    person_near = check_people_near() # take 2 seconds
    others = Others(us_dist=str(int(us_dist))+"cm", voltage=voltage,person_near=person_near)
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
