from fastapi import FastAPI, Form
from fastapi.responses import Response
import sys

sys.path.append('../client')
from server_utils.path import ULTRASOUND_DATA
from formats.states_format import Obstacle, ObstacleInput

app = FastAPI()


@app.post("/ultrasound/")
async def receive_ultrasound(data: ObstacleInput):
    obstacle = Obstacle(dist=data.dist)
    f = open(ULTRASOUND_DATA, 'w', encoding='utf-8')
    f.write(obstacle.dist + "\n")
    f.close()
    print(obstacle.dist + "\n")  # async write
    return Response(status_code=200)
