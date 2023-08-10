from fastapi import FastAPI, Form
from fastapi.responses import Response
import sys
import json

sys.path.append('../client')
from server_utils.path import OTHERS_DATA
from formats.states_format import Others, OthersInput

app = FastAPI()


@app.post("/others/")
async def receive(data: OthersInput):
    others = Others(up_dist=data.up_dist, voltage=data.voltage, person_near=data.person_near,
                    head_hori=data.head_hori, head_vert=data.head_vert, body_direct=data.body_direct,
                    last_async_task=data.last_async_task, last_async_task_state=data.last_async_task_state, last_async_task_result=data.last_async_task_result)
    f = open(OTHERS_DATA, 'w', encoding='utf-8')
    f.write(json.dumps(vars(others), ensure_ascii=False))
    f.close()
    print(others)  # async write
    return Response(status_code=200)
