import time
import cv2


def wait_for_static(tm=3):
    time.sleep(tm)


def set_camera(cap, cap_id=0):
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 75 if cap_id == 0 else 20)  # 亮度 130
    cap.set(cv2.CAP_PROP_CONTRAST, 64)  # 对比度 32
    cap.set(cv2.CAP_PROP_SATURATION, 64)  # 饱和度 64
    cap.set(cv2.CAP_PROP_HUE, 0)  # 色调 0
    cap.set(cv2.CAP_PROP_EXPOSURE, -4)  # 曝光 -4
