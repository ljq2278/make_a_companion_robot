import cv2
import requests
import time
import numpy as np

# Set the server URL (adjust the IP address and port if needed)
SERVER_URL = "http://192.168.1.9:8002/vision/"

cap = cv2.VideoCapture(0)
time_per_frame = 2 / 1


def send_image():
    ret, frame = cap.read()
    if not ret:
        return ""
    _, image_encoded = cv2.imencode(".jpg", frame)
    image_bytes = image_encoded.tobytes()
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    print('send image ...')
    response = requests.post(SERVER_URL, files=files)
    print('Response:', response.status_code, response.text)


if __name__ == "__main__":
    # Change the '0' to the appropriate camera ID if needed
    recv_order = ""
    try:
        while cap.isOpened():
            time.sleep(0.5)
            send_image()
    finally:
        cap.release()
