import time
from client_utils.path import ASYNC_TASK_FLG
import json
import os


def wait_for_static(tm=3):
    time.sleep(tm)


def get_task_state():
    while True:
        try:
            res = json.load(open(ASYNC_TASK_FLG, 'r', encoding='utf-8'))
            return res
        except Exception as e:
            print(e)


def set_task_state(nm, state, result):
    json.dump({"last_async_task": nm, "last_async_task_state": state, "last_async_task_result": result}, open(ASYNC_TASK_FLG, 'w', encoding='utf-8'))

# def lock(file_path):
#     lock_path = "/".join(file_path.split("/")[:-1] + ["lock"])
#     f = open(lock_path, 'w', encoding='utf-8')
#     f.close()
#
#
# def unlock(file_path):
#     lock_path = "/".join(file_path.split("/")[:-1] + ["lock"])
#     try:
#         os.remove(lock_path)
#     except Exception as e:
#         print(e)
