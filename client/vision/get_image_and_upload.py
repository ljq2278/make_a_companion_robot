import cv2
import requests
import time

# Set the server URL (adjust the IP address and port if needed)
SERVER_URL = "http://192.168.1.8:8001/detect/"


def send_image(image):
    _, image_encoded = cv2.imencode(".jpg", image)
    image_bytes = image_encoded.tobytes()
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    response = requests.post(SERVER_URL, files=files)

    if response.status_code == 200:
        detected_objects = response.json()["objects"]
        for obj in detected_objects:
            print(f"- {obj['name']} at bbox {obj['bbox']}")
        print('this frame end')
    else:
        print(f"Error: {response.status_code} - {response.text}")


def capture_and_send_images(cam_id, fps):
    cap = cv2.VideoCapture(cam_id)
    time_per_frame = 2 / fps

    try:
        while cap.isOpened():
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break

            send_image(frame)

            elapsed_time = time.time() - start_time
            sleep_time = max(0, time_per_frame - elapsed_time)
            time.sleep(sleep_time)
    finally:
        cap.release()


if __name__ == "__main__":
    # Change the '0' to the appropriate camera ID if needed
    capture_and_send_images(cam_id=0, fps=10)
