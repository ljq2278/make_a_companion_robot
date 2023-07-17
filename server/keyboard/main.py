from fastapi import FastAPI, Form
from fastapi.responses import Response
from pydantic import BaseModel
import aiofiles

app = FastAPI()
output_txt_file = "./auditory/record.txt"


class Item(BaseModel):
    text: str


@app.post("/keyborad/")
async def receive_audio(text: str = Form(...)):
    print(text)
    async with aiofiles.open(output_txt_file, 'w', encoding='utf-8') as out_file:
        await out_file.write(text)  # async write
    return Response(status_code=200)
