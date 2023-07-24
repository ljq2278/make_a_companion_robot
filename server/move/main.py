import io
from PIL import Image
import os
from typing import Union
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import logging
from utils.path import MOVE_ACTION_FILE, MOVE_ACTION_COMPLETE_FILE

logging.basicConfig(level=logging.DEBUG)
# from yolov5.yolo import YOLO
from ultralytics import YOLO

app = FastAPI()

# output_txt_file = MOVE_ACTION_RESULT_FILE
input_txt_file = MOVE_ACTION_FILE
action_complete_file = MOVE_ACTION_COMPLETE_FILE
last_modify_time = None

@app.post("/move/")
async def detect_objects(complete: str = Form(...)):
    global last_modify_time, input_txt_file
    action = ""
    # f = open(output_txt_file, 'w', encoding='utf-8')
    # f.write(on_move + "\n")
    # f.close()
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
