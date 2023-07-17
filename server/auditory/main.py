

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import aiofiles
import whisper


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
