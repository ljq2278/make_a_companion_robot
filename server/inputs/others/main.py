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
    others = Others(us_dist=data.us_dist, voltage=data.voltage, person_near=data.person_near)
    f = open(OTHERS_DATA, 'w', encoding='utf-8')
    f.write(json.dumps(vars(others), ensure_ascii=False))
    f.close()
    print(others)  # async write
    return Response(status_code=200)
