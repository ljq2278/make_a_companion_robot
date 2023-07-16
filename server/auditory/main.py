# import whisper
#
# model = whisper.load_model("base")
# result = model.transcribe("audio.wav")
#
# @app.post("/auditory/")
# async def detect_objects(file: UploadFile = File(...)):
#     logging.debug("Image received")
#
#     # Load the image from the uploaded file
#     image_data = await file.read()
#     image = Image.open(io.BytesIO(image_data)).convert("RGB")
#     # image_tensor = torchvision.transforms.ToTensor()(image)
#
#     logging.debug("Image loaded")
#
#     # Perform object detection using the YOLO model
#     results = model(image)
#     # logging.debug('len: ',len(results))
#     logging.debug("Object detection performed")
#
#     # Extract object names and bounding boxes
#     objects = []
#     # for detection in results.xyxy[0]:
#     #     x1, y1, x2, y2, conf, cls = detection.tolist()
#     #     name = model.names[int(cls)]
#     #     objects.append({"name": name, "bbox": [x1, y1, x2, y2]})
#     #     logging.debug(f"Detected object: {name}, bbox: [{x1}, {y1}, {x2}, {y2}]")
#     for i in range(0, len(results[0].boxes.xyxy.tolist())):
#         x1, y1, x2, y2 = results[0].boxes.xyxy.tolist()[i]
#         name = model.names[results[0].boxes.cls.tolist()[i]]
#         objects.append({"name": name, "bbox": [x1, y1, x2, y2]})
#     return JSONResponse(content={"objects": objects})
import os
import time

import ffmpeg
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import aiofiles
import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read

app = FastAPI()
model = whisper.load_model("base.en")
output_wav_file = "./auditory/record.wav"
output_txt_file = "./auditory/record.txt"


@app.post("/auditory/")
async def receive_audio(file: UploadFile = File(...)):
    # Save the audio file
    # try:
    #     os.remove(output_wav_file)
    # except Exception as e:
    #     print(e)
    async with aiofiles.open(output_wav_file, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    # time.sleep(1)
    result = model.transcribe(output_wav_file)
    print(result["text"])
    async with aiofiles.open(output_txt_file, 'w', encoding='utf-8') as out_file:
        await out_file.write(result["text"])  # async write
    return Response(status_code=200)
