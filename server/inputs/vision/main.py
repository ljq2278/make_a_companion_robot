import io
import time

from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form
import logging
from fastapi.responses import Response, PlainTextResponse, JSONResponse
import subprocess
import torch

from server_utils.path import MODEL_PATH, VISION_DATA

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Initialize the YOLO model
model = torch.hub.load("ultralytics/yolov5", "yolov5m")
model.to("cpu")
output_txt_file = VISION_DATA
img_procs = []


def show_imgs(results):
    results.render()
    im = results.ims[0]
    tmp = Image.fromarray(im)
    tmp.save("tmp.png", format="JPEG")
    # tmp = Image.fromarray(res_plotted, mode="RGB")
    # tmp.save("tmp.png")
    p = subprocess.Popen("python inputs/vision/test/image_viewer.py tmp.png")
    if len(img_procs) == 2:
        tmp = img_procs.pop(0)
        tmp.kill()
    img_procs.append(p)


def show_cur_img(results):
    results.render()
    im = results.ims[0]
    tmp = Image.fromarray(im)
    tmp.save("tmp.png", format="JPEG")
    # tmp = Image.fromarray(res_plotted, mode="RGB")
    # tmp.save("tmp.png")
    p = subprocess.Popen("python inputs/vision/test/image_viewer.py tmp.png")
    time.sleep(1)
    p.kill()


@app.post("/vision/")
async def detect_objects(file: UploadFile = File(...), text: str = Form(...)):
    global img_procs

    logging.debug("Image received")

    # Load the image from the uploaded file
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    logging.debug("Image loaded")

    # Perform object detection using the YOLO model
    results = model(image)
    if text == "consecutive":
        show_imgs(results)
    elif text == "single":
        show_cur_img(results)
    # logging.debug('len: ',len(results))
    logging.debug("Object detection performed")

    objects = []
    f = open(output_txt_file, 'w', encoding='utf-8')
    xyxyn = results.pandas().xyxyn[0]
    for i in range(0, len(xyxyn)):

        if xyxyn.loc[i, "confidence"] > 0.1:
            objects.append({"name": xyxyn.loc[i, "name"], "bbox": [xyxyn.loc[i, "xmin"], xyxyn.loc[i, "ymin"], xyxyn.loc[i, "xmax"], xyxyn.loc[i, "ymax"]]})
            f.write(xyxyn.loc[i, "name"] + "\n")
    f.close()
    # return Response(status_code=200)
    return JSONResponse(status_code=200, content=objects)
