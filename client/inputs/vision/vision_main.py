import cv2
import requests
import os
from PIL import Image
import numpy as np
from client_utils.path import VISION_SERVER_IP_PATH, CAMERA_IMG_PATH, PHYSICS_PARAM_BLACK_CAMERA

cap_id = 1
cap1 = cv2.VideoCapture(cap_id)
show_img_type = "none"  # consecutive, single


def set_camera(cap):
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 75 if cap_id == 0 else 10)  # 亮度 130
    cap.set(cv2.CAP_PROP_CONTRAST, 24)  # 对比度 32
    cap.set(cv2.CAP_PROP_SATURATION, 24)  # 饱和度 64
    cap.set(cv2.CAP_PROP_HUE, 0)  # 色调 0
    cap.set(cv2.CAP_PROP_EXPOSURE, -4)  # 曝光 -4
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    # cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    # # 设置曝光为手动模式

    # # # 设置曝光的值为0
    # print(cap.set(cv2.CAP_PROP_EXPOSURE, 100))
    # cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)
    # cap.set(cv2.CAP_PROP_EXPOSURE, -1)  # 曝光 -4
    # cap.set(cv2.CAP_PROP_BRIGHTNESS, 15)
    # cap.set(cv2.CAP_PROP_CONTRAST, 40)
    # cap.set(cv2.CAP_PROP_SATURATION, 50)
    # cap.set(cv2.CAP_PROP_HUE, 50)
    if os.path.exists(PHYSICS_PARAM_BLACK_CAMERA):
        cap.set(cv2.CAP_PROP_EXPOSURE, 0)  # 黑夜模式，只能看到强光源
    return


def save_frame(frame):
    img = Image.fromarray(frame)
    img.save(CAMERA_IMG_PATH, format="JPEG")


def send_image():
    global cap1
    cap1.release()
    cap1 = cv2.VideoCapture(cap_id)
    set_camera(cap1)
    ret, frame = cap1.read()
    # frame = np.power(frame.astype(float), 0.9).astype(np.uint8)
    save_frame(frame)
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
            # time.sleep(0.5)
            send_image()
    finally:
        cap1.release()
