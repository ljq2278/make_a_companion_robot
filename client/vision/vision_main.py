import cv2
import requests
import time
from adafruit_servokit import ServoKit
import numpy as np

# Set the server URL (adjust the IP address and port if needed)
SERVER_URL = "http://192.168.1.9:8002/vision/"

kit = ServoKit(channels=16)
cap = cv2.VideoCapture(0)
time_per_frame = 2 / 1
param_to_angle = {
    "look_ahead": 90,
    "look_at_left": 135,
    "look_at_right": 45,
    "look_around": -90,
}
turn_angle_speed = 5


def turn_angle(src, dest):
    for angle in np.arange(src, dest, turn_angle_speed if dest > src else -turn_angle_speed):
        kit.servo[3].angle = angle
        time.sleep(0.1)


def act_and_send_image(param):
    global kit
    param = param.strip()
    if param in param_to_angle.keys():
        kit.servo[3].angle = 90
        start_angle = kit.servo[3].angle
        if param_to_angle[param] > 0:
            if param_to_angle[param] != 90:
                turn_angle(start_angle, param_to_angle[param])
            kit.servo[3].angle = None
            time.sleep(1)
            send_image(complete='true')
        else:  # look_around
            turn_angle(start_angle, 45)
            time.sleep(1)
            send_image()
            turn_angle(45, 135)
            time.sleep(1)
            send_image()
            turn_angle(135, 90)
            kit.servo[3].angle = None
            time.sleep(1)
            send_image(complete='true')
        return ""
    else:
        print("invalid param: ", param)
        return ""


def send_image(complete="false"):
    ret, frame = cap.read()
    if not ret:
        return ""
    _, image_encoded = cv2.imencode(".jpg", frame)
    image_bytes = image_encoded.tobytes()
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    print('send image ...')
    response = requests.post(SERVER_URL, files=files, data= {'complete': complete})
    if response.status_code == 200:
        action = response.json()["action"]
        print('get action: ', action)
        return action
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ""


if __name__ == "__main__":
    # Change the '0' to the appropriate camera ID if needed
    recv_order = ""
    try:
        while cap.isOpened():
            start_time = time.time()
            if recv_order == "":
                recv_order = send_image()
            else:
                recv_order = act_and_send_image(recv_order)
            elapsed_time = time.time() - start_time
            sleep_time = max(0, time_per_frame - elapsed_time)
            time.sleep(sleep_time)
    finally:
        cap.release()
