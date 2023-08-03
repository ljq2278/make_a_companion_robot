
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, Response
import logging
from action.physical.look import look_funcs, l_init, unset_motor
from action.physical.say import read_alound_and_show_text
from action.physical.show_mood import show_mood
from action.async_logical.explore import one_time_explore
import subprocess
logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

async_explore_pid = None

@app.on_event("startup")
def startup_event():
    print("start the server ...")
    l_init()


@app.on_event("shutdown")
def shutdown_event():
    print("stop the server ...")
    unset_motor()

    # Perform your postprocess tasks here


@app.post("/action/")
async def do_action(action: str = Form(...)):
    global async_explore_pid
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
        elif act == "explore":
            async_explore_pid = subprocess.Popen("python3 action/async_logical/explore.py")
        else:
            return Response(status_code=200, content="false")
        return Response(status_code=200, content="true")
    except Exception as e:
        print(e)
        return Response(status_code=200, content="false")
        # return JSONResponse(content={"text": "false"})


if __name__ == '__main__':
    show_mood("curious")
