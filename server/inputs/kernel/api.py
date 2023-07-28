from server_utils.path import KERNEL_DATA
import json


def get_kernel_data():
    res = {}
    try:
        f = open(KERNEL_DATA, 'r', encoding='utf-8')
        res = json.loads([line.strip() for line in f.readlines()][0])
        f.close()
    except Exception as e:
        print(e)
    return res
