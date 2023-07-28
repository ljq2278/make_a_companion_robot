from fastapi import FastAPI, Form
from fastapi.responses import Response
import aiofiles
from server_utils.path import KEYBOARD_DATA

app = FastAPI()


@app.post("/keyborad/")
async def receive_audio(text: str = Form(...)):
    print(text)
    async with aiofiles.open(KEYBOARD_DATA, 'w', encoding='utf-8') as out_file:
        await out_file.write(text)  # async write
    return Response(status_code=200)
