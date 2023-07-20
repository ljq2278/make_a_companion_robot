import io
from PIL import Image
import os
from typing import Union
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import logging
from utils.path import ACTION_FILE, ACTION_COMPLETE_FILE, VISION_RESULT_FILE, MODEL_PATH

logging.basicConfig(level=logging.DEBUG)
# from yolov5.yolo import YOLO
from ultralytics import YOLO

app = FastAPI()

# Initialize the YOLO model
# model = YOLO.from_pretrained("../../yolov8x.pt")
model = YOLO(MODEL_PATH+"yolov8m.pt")
model.to("cpu")
output_txt_file = VISION_RESULT_FILE
input_txt_file = ACTION_FILE
action_complete_file = ACTION_COMPLETE_FILE
last_modify_time = None


@app.post("/vision/")
async def detect_objects(file: UploadFile = File(...), complete: str = Form(...)):
    global last_modify_time, input_txt_file
    print("file: ", file.filename, "\n")
    print("name: ", complete, "\n")
    logging.debug("Image received")

    # Load the image from the uploaded file
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    # image_tensor = torchvision.transforms.ToTensor()(image)

    logging.debug("Image loaded")

    # Perform object detection using the YOLO model
    results = model(image)
    # logging.debug('len: ',len(results))
    logging.debug("Object detection performed")

    # Extract object names and bounding boxes
    objects = []
    action = ""

    f = open(output_txt_file, 'w', encoding='utf-8')
    for i in range(0, len(results[0].boxes.xyxy.tolist())):
        x1, y1, x2, y2 = results[0].boxes.xyxy.tolist()[i]
        name = model.names[results[0].boxes.cls.tolist()[i]]
        objects.append({"name": name, "bbox": [x1, y1, x2, y2]})
        f.write(name + "\n")
    f.close()
    if complete == "true":
        f = open(action_complete_file, 'w', encoding='utf-8')
        f.write("1")
        f.close()
    if input_txt_file is None or os.path.getmtime(input_txt_file) != last_modify_time:
        f = open(input_txt_file, 'r', encoding='utf-8')
        action = f.read()
        f.close()
        last_modify_time = os.path.getmtime(input_txt_file)
    # return JSONResponse(content={"objects": objects})
    return JSONResponse(content={"action": action})
