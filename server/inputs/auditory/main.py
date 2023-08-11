from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from server_utils.path import AUDITORY_DATA, AUDITORY_RAW_DATA
import aiofiles
import whisper

app = FastAPI()
model = whisper.load_model("base.en")


@app.post("/auditory/")
async def receive_audio(file: UploadFile = File(...)):
    # Save the audio file
    # try:
    #     os.remove(output_wav_file)
    # except Exception as e:
    #     print(e)
    async with aiofiles.open(AUDITORY_RAW_DATA, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    # time.sleep(1)
    result = model.transcribe(AUDITORY_RAW_DATA)
    print(result["text"])
    async with aiofiles.open(AUDITORY_DATA, 'w', encoding='utf-8') as out_file:
        await out_file.write(result["text"])  # async write
    return Response(status_code=200)
