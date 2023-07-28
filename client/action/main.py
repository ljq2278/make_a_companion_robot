import time
from PIL import Image
import os
from typing import Union
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse,Response
import logging
from action.physical.look import look_funcs
from action.physical.say import read_alound_and_show_text
from action.physical.show_mood import show_mood

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()


@app.post("/action/")
async def do_action(action: str = Form(...)):
    try:
        print(action)
        action_full = action.split("#")
        act = action_full[0]
        act_param = ""
        if len(action_full)==2:
            act_param = action_full[1]
        if act in look_funcs.keys():
            look_funcs[act]()
        elif act == "show_mood":
            show_mood(act_param)
        elif act == "say":
            read_alound_and_show_text(act_param)
        else:
            return Response(status_code=200, content="false")
        return Response(status_code=200,content="true")
    except Exception as e:
        print(e)
        return Response(status_code=200, content="false")
        # return JSONResponse(content={"text": "false"})

if __name__ == '__main__':
    show_mood("curious")