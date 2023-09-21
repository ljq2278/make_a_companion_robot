
import requests, copy
from client_utils.path import KEYBOARD_SERVER_IP_PATH
# Find the correct event number for your USB keyboard in /dev/input

if __name__ == '__main__':
    while True:
        text = input()
        print('Sending:', text)
        response = requests.post(KEYBOARD_SERVER_IP_PATH, data={'text': text})
        print('Response:', response.status_code, response.text)
