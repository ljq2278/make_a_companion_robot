import cv2
import requests
import time
import numpy as np
from client_utils.path import VISION_SERVER_IP_PATH

cap_id = 1
cap1 = cv2.VideoCapture(cap_id)
show_img_type = "none" # consecutive, single

def set_camera(cap):
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 75 if cap_id==0 else 20)  # 亮度 130
    cap.set(cv2.CAP_PROP_CONTRAST, 64)  # 对比度 32
    cap.set(cv2.CAP_PROP_SATURATION, 64)  # 饱和度 64
    cap.set(cv2.CAP_PROP_HUE, 0)  # 色调 0
    cap.set(cv2.CAP_PROP_EXPOSURE, -4)  # 曝光 -4


def send_image():
    global cap1
    cap1.release()
    cap1 = cv2.VideoCapture(cap_id)
    set_camera(cap1)
    ret, frame = cap1.read()
    _, image_encoded = cv2.imencode(".jpg", frame)
    image_bytes = image_encoded.tobytes()
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    print('send image ...')
    response = requests.post(VISION_SERVER_IP_PATH, files=files, data={'text': show_img_type})
    print('Response:', response.status_code, response.text)


if __name__ == "__main__":
    # Change the '0' to the appropriate camera ID if needed
    recv_order = ""
    try:
        while cap1.isOpened():
            time.sleep(0.5)
            send_image()
    finally:
        cap1.release()
