import io
from PIL import Image
import torch
import torchvision
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.DEBUG)
# from yolov5.yolo import YOLO
from ultralytics import YOLO

app = FastAPI()

# Initialize the YOLO model
# model = YOLO.from_pretrained("../../yolov8x.pt")
model = YOLO("../../../models/yolov8n.pt")


@app.post("/vision/")
async def detect_objects(file: UploadFile = File(...)):
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
    # for detection in results.xyxy[0]:
    #     x1, y1, x2, y2, conf, cls = detection.tolist()
    #     name = model.names[int(cls)]
    #     objects.append({"name": name, "bbox": [x1, y1, x2, y2]})
    #     logging.debug(f"Detected object: {name}, bbox: [{x1}, {y1}, {x2}, {y2}]")
    for i in range(0, len(results[0].boxes.xyxy.tolist())):
        x1, y1, x2, y2 = results[0].boxes.xyxy.tolist()[i]
        name = model.names[results[0].boxes.cls.tolist()[i]]
        objects.append({"name": name, "bbox": [x1, y1, x2, y2]})
    return JSONResponse(content={"objects": objects})
