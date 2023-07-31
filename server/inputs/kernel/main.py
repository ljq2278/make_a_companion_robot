from fastapi import FastAPI, Form
from fastapi.responses import Response
import sys

sys.path.append('../client')
from server_utils.path import KERNEL_DATA
from formats.states_format import Kernel, KernelInput

app = FastAPI()


@app.post("/kernel/")
async def receive(data: KernelInput):
    kernel = Kernel(voltage=data.voltage)
    f = open(KERNEL_DATA, 'w', encoding='utf-8')
    f.write(kernel.voltage + "\n")
    f.close()
    print(kernel.voltage + "\n")  # async write
    return Response(status_code=200)
