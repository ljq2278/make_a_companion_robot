from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, Response
import logging
from action.physical.look import look_funcs, l_init, unset_motor
from action.physical.say import read_alound_and_show_text
from action.physical.show_mood import show_mood
# from action.physical.move_and_rotate import r_right
# from action.async_logical.exploreWorld import one_time_explore
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
    l_init()
    show_mood("happy")
    read_alound_and_show_text("time to get up!")


@app.on_event("shutdown")
def shutdown_event():
    print("stop the server ...")
    unset_motor()

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
        if act in look_funcs.keys():
            look_funcs[act]()
        elif act == "show_mood":
            show_mood(act_param)
        elif act == "say":
            read_alound_and_show_text(act_param)
        elif act in async_task_set:
            try:
                async_pid.kill()
            except Exception as e:
                print(e)
            set_task_state(act, "on doing", "")
            async_pid = subprocess.Popen(["python3", "/home/pi/Code/client/action/async_logical/%s.py" % act, act_param])
        else:
            return Response(status_code=200, content="false")
        return Response(status_code=200, content="true")
    except Exception as e:
        print(e)
        return Response(status_code=200, content="false")


if __name__ == '__main__':
    # show_mood("curious")
    act = "findPersonChat"
    act_param = "Hi there! Do you want to chat? [polite]"
    async_pid = subprocess.Popen(["python3", "/home/pi/Code/client/action/async_logical/%s.py" % act, act_param])
    print(async_pid)
    import time

    time.sleep(100000)
