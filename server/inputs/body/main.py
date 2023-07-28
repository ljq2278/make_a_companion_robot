import json

from fastapi import FastAPI, Form
from fastapi.responses import Response
import sys

sys.path.append('../client')
from server_utils.path import BODY_DATA
from formats.states_format import Body, BodyInput

app = FastAPI()


@app.post("/body/")
async def receive_ultrasound(data: BodyInput):
    body = Body(hori_rot=data.hori_rot, vert_rot=data.vert_rot)
    f = open(BODY_DATA, 'w', encoding='utf-8')
    f.write(json.dumps(vars(body), ensure_ascii=False))
    f.close()
    print(json.dumps(vars(body), ensure_ascii=False) + "\n")  # async write
    return Response(status_code=200)
