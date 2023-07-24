import io
from PIL import Image
import os
from typing import Union
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import logging
from utils.path import ACTION_FILE, ACTION_RESULT_FILE, ACTION_FLAG_FILE
from action.lib.get_result import get_vision_result, get_move_result, get_rotate_result

logging.basicConfig(level=logging.DEBUG)
# from yolov5.yolo import YOLO
from ultralytics import YOLO

app = FastAPI()

# output_txt_file = MOVE_ACTION_RESULT_FILE
action_file = ACTION_FILE
action_result_file = ACTION_RESULT_FILE
last_modify_time = ""
cur_action = ""


def create_action_flag():
    f = open(ACTION_FLAG_FILE, 'w', encoding='utf-8')
    f.write("1")
    f.close()


def delete_action_flag():
    try:
        os.remove(ACTION_FLAG_FILE)
    except Exception as e:
        print(e)


@app.post("/action/")
async def do_action(state: str = Form(...)):
    global last_modify_time, action_file, cur_action
    if state == "complete":
        res = ""
        if cur_action == "look":
            res = get_vision_result()
        elif cur_action == "move":
            res = get_move_result()
        elif cur_action == "rotate":
            res = get_rotate_result()
        print(res)
        f = open(action_result_file, 'w', encoding='utf-8')
        f.write(res)
        f.close()
        delete_action_flag()
    if os.path.getmtime(action_file) != last_modify_time:
        f = open(action_file, 'r', encoding='utf-8')
        cur_action = f.read()
        f.close()
        last_modify_time = os.path.getmtime(action_file)
        create_action_flag()
        return JSONResponse(content={"action": cur_action})
    else:
        return JSONResponse(content={"action": ""})
