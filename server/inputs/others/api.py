from server_utils.path import OTHERS_DATA
import json

def get_others_dict():
    try:
        res = json.load(open(OTHERS_DATA, 'r', encoding='utf-8'))
        return res
    except Exception as e:
        print(e)
        return {}


