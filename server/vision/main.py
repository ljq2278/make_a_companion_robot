import io
import time

from PIL import Image
import os
from typing import Union
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import logging
from utils.path import MODEL_PATH, VISION_DATA
from fastapi.responses import Response
import cv2
import subprocess

logging.basicConfig(level=logging.DEBUG)
# from yolov5.yolo import YOLO
from ultralytics import YOLO

app = FastAPI()

# Initialize the YOLO model
# model = YOLO.from_pretrained("../../yolov8x.pt")
model = YOLO(MODEL_PATH + "yolov8m.pt")
model.to("cpu")
output_txt_file = VISION_DATA
last_modify_time = None
img_procs = []


@app.post("/vision/")
async def detect_objects(file: UploadFile = File(...)):
    global last_modify_time, img_procs

    logging.debug("Image received")

    # Load the image from the uploaded file
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    logging.debug("Image loaded")

    # Perform object detection using the YOLO model
    results = model(image)
    # logging.debug('len: ',len(results))
    logging.debug("Object detection performed")
    res_plotted = results[0].plot()
    tmp = Image.fromarray(res_plotted, mode="RGB")
    tmp.save("tmp.png")
    p = subprocess.Popen("python vision/test/image_viewer.py tmp.png")
    if len(img_procs) == 2:
        tmp = img_procs.pop(0)
        tmp.kill()
    img_procs.append(p)
    # res_plotted.show("result", res_plotted)
    # Extract object names and bounding boxes
    objects = []
    f = open(output_txt_file, 'w', encoding='utf-8')
    for i in range(0, len(results[0].boxes.xyxy.tolist())):
        x1, y1, x2, y2 = results[0].boxes.xyxy.tolist()[i]
        name = model.names[results[0].boxes.cls.tolist()[i]]
        conf = results[0].boxes.conf.tolist()[i]
        if conf > 0.5:
            objects.append({"name": name, "bbox": [x1, y1, x2, y2]})
            f.write(name + "\n")
    f.close()
    # return JSONResponse(content={"objects": objects})
    return Response(status_code=200)
