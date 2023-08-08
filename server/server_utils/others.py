import time
from inputs.vision.api import get_objs
from inputs.keyboard.api import get_keyboard_input
from inputs.others.api import get_others_dict
import json

task_priorities = {
    "exploreWorld": 0,
    "findObj": 1,
    "findPersonChat": 2,
    "goCharge": 3
}


def parse_txt_and_mood(txt):
    txt = txt.strip().split("\n")[0]
    res = {"speech": txt, "mood": "normal"}
    tmp = txt.split(']')
    if len(tmp) < 2:
        return res
    tmp = ''.join(tmp[:-1])
    tmp = tmp.split('[')
    if len(tmp) < 2:
        return res
    res["speech"] = ''.join(tmp[:-1])
    res["mood"] = tmp[-1]
    return res


def wait_for_human_response(tm=20):
    time.sleep(tm)


def get_async_task_info():
    while True:
        try:
            res = get_others_dict()
            break
        except Exception as e:
            print(e)
    return res["last_async_task"], res["last_async_task_state"], res["last_async_task_result"]


def get_states():
    res = get_others_dict()
    res.update(
        {
            "head vision": get_objs(),
        }
    )
    res.update(
        {
            "human message": get_keyboard_input(),
        }
    )
    return res


def get_nl_states():
    res = get_states()
    del res["us_dist"]
    if res["voltage"] <= 6.5:
        res["voltage"] = "low"
    else:
        res["voltage"] = "sufficient"
    return res


if __name__ == '__main__':
    get_nl_states()
