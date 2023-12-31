import time
import requests
from inputs.vision.api import get_objs
from inputs.keyboard.api import get_keyboard_input
from inputs.auditory.api import get_auditory_input
from inputs.others.api import get_others_dict
from server_utils.path import CLIENT_ACTION_IP_PATH

task_priorities = {
    "exploreWorld": 0,
    "findObj": 1,
    "findPersonChat": 2,
    "goCharge": 3
}


def send_message(addr, data):
    response = requests.post(addr, data=data)
    return response


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


def wait_for_human_response(tm=10):
    time.sleep(tm)


def get_async_task_info():
    while True:
        try:
            res = get_others_dict()
            break
        except Exception as e:
            print(e)
    return res["last_async_task"], res["last_async_task_state"], res["last_async_task_result"]


def get_async_task_return(cur_task, query):
    task_nm, task_state, task_res = get_async_task_info()
    if task_state == "on doing" and task_priorities[task_nm] >= task_priorities[cur_task]:
        res = task_nm + " is still on doing, current task can not be started. "
    else:
        response = send_message(CLIENT_ACTION_IP_PATH, data={'action': cur_task + "#" + query})
        if response.status_code == 200:
            res = "start task <%s>, result can be checked later in the information from sensors. " % cur_task
        else:
            res = "something wrong with task startup, try it later. "
    print("observation: " + res)
    return res


class States:

    def __init__(self):
        self.last_states = None

    def get_states(self):
        res = get_others_dict()
        res.update(
            {
                "vision": get_objs(),
            }
        )
        res.update(
            {
                "human keyboard message": get_keyboard_input(),
            }
        )
        res.update(
            {
                "human oral message": get_auditory_input(),
            }
        )
        return res

    def get_nl_states(self):
        res = self.get_states()
        del res["up_dist"]
        if res["voltage"] <= 6.5:
            res["voltage"] = "low"
        else:
            res["voltage"] = "sufficient"
        return res

    def get_critical_states(self):
        res = self.get_nl_states()
        if self.last_states is None:
            self.last_states = res
            return res
        else:
            res_diff = {}
            for k, v in res.items():
                if self.last_states[k] != v:
                    res_diff[k] = v
            if res["voltage"] == "low":
                res_diff["voltage"] = "low"
            self.last_states = res
            return res_diff


if __name__ == '__main__':
    States().get_nl_states()
