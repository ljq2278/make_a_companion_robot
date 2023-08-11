import sys
sys.path.append(r'/home/pi/Code/client')

import cv2
import requests
import os
from PIL import Image

from client_utils.path import VISION_SERVER_IP_PATH, CAMERA_IMG_PATH, PHYSICS_PARAM_BLACK_CAMERA


def set_camera(cap):
    # cap.set(cv2.CAP_PROP_FPS, 20)
    # print("CAP_PROP_FPS: ", cap.get(cv2.CAP_PROP_FPS))
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
    # print("CAP_PROP_FOURCC: ", cap.get(cv2.CAP_PROP_FOURCC))
    # cap.set(6, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('m', 'j', 'p', 'g'))
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # cap.set(cv2.CAP_PROP_BRIGHTNESS, 75 if cap_id == 0 else 10)  # 亮度 130
    # cap.set(cv2.CAP_PROP_BRIGHTNESS, 20)
    print("CAP_PROP_BRIGHTNESS: ", cap.get(cv2.CAP_PROP_BRIGHTNESS))
    cap.set(cv2.CAP_PROP_CONTRAST, 32)  # 对比度 32
    print("CAP_PROP_CONTRAST: ", cap.get(cv2.CAP_PROP_CONTRAST))
    cap.set(cv2.CAP_PROP_SATURATION, 64)  # 饱和度 64
    print("CAP_PROP_SATURATION: ", cap.get(cv2.CAP_PROP_SATURATION))
    cap.set(cv2.CAP_PROP_HUE, 0)  # 色调 0
    cap.set(cv2.CAP_PROP_EXPOSURE, -4)  # 曝光 -4

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


cap_id = 0
# cap_id += + cv2.CAP_DSHOW
cap1 = cv2.VideoCapture(cap_id)
# os.system("bash ~/camera.sh")
set_camera(cap1)
# subprocess.Popen(["/usr/bin/uvcdynctrl", " -d /dev/video1 -S 6:10 '(LE)0x0400'"])
# time.sleep(1)
show_img_type = "none"  # consecutive, single
send_frame_rate = 24


def save_frame(frame):
    img = Image.fromarray(frame)
    img.save(CAMERA_IMG_PATH, format="JPEG")


def send_image(cont):
    global cap1
    print("CAP_PROP_FPS: ", cap1.get(cv2.CAP_PROP_FPS))
    print("read start ###########################")
    ret, frame = cap1.read()
    print("read end ###########################")
    if cont % send_frame_rate == 0:
        save_frame(frame)
        _, image_encoded = cv2.imencode(".jpg", frame)
        image_bytes = image_encoded.tobytes()
        files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
        print('send image ...')
        response = requests.post(VISION_SERVER_IP_PATH, files=files, data={'text': show_img_type})
        print('Response:', response.status_code, response.text)
    else:
        return


if __name__ == "__main__":
    # Change the '0' to the appropriate camera ID if needed
    recv_order = ""
    cont = 0
    try:
        while cap1.isOpened():
            send_image(cont)
            cont += 1
    finally:
        cap1.release()
