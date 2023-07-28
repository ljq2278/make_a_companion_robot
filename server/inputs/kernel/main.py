from fastapi import FastAPI, Form
from fastapi.responses import Response
import aiofiles
from server_utils.path import KERNEL_DATA

app = FastAPI()


@app.post("/kernel/")
async def receive(text: str = Form(...)):
    print(text)
    async with aiofiles.open(KERNEL_DATA, 'w', encoding='utf-8') as out_file:
        await out_file.write(text)  # async write
    return Response(status_code=200)
