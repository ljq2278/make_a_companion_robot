from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, Response
import logging
from action.physical.say import read_alound_and_show_text
from action.physical.show_mood import show_mood
from client_utils.others import set_task_state
import subprocess
import sys

sys.path.append(r'/home/pi/Code/client')

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
async_task_set = {"findObj", "goCharge", "exploreWorld", "findPersonChat"}
async_pid = None


@app.on_event("startup")
def startup_event():
    print("start the server ...")
    show_mood("happy")
    read_alound_and_show_text("time to get up!")


@app.on_event("shutdown")
def shutdown_event():
    print("stop the server ...")
    # Perform your postprocess tasks here


@app.post("/action/")
async def do_action(action: str = Form(...)):
    global async_pid
    try:
        print(action)
        action_full = action.split("#")
        act = action_full[0]
        act_param = ""
        if len(action_full) == 2:
            act_param = action_full[1]
        if act == "show_mood":
            show_mood(act_param)
        elif act == "say":
            read_alound_and_show_text(act_param)
        else:
            return Response(status_code=200, content="false")
        return Response(status_code=200, content="true")
    except Exception as e:
        print(e)
        return Response(status_code=200, content="false")


if __name__ == '__main__':
    # show_mood("curious")
    actn = "findPersonChat"
    actn_param = "Hi there! Do you want to chat? [polite]"
    async_pid = subprocess.Popen(["python3", "/home/pi/Code/client/action/async_logical/%s.py" % actn, actn_param])
    print(async_pid)
    import time

    time.sleep(100000)
