# server.py
from fastapi import FastAPI
import json
import os
app = FastAPI()

data_path = "agent/v1/saved/current.txt"
last_modify_time = None
@app.get("/expression/")
async def get_data():
    # Replace this with your actual data source
    global last_modify_time, data_path
    if data_path is None or os.path.getmtime(data_path) != last_modify_time:
        last_modify_time = os.path.getmtime(data_path)
        data = json.load(open(data_path,'r',encoding='utf-8'))
        data_str = json.dumps(data)
        print(data_str)
        return {"data": data_str}
    else:
        print("no data")
        return {"data": ""}