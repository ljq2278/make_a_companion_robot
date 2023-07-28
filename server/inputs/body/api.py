from server_utils.path import BODY_DATA
import json


def get_body():
    try:
        f = open(BODY_DATA, 'r', encoding='utf-8')
        res = json.loads(f.read())
        f.close()
        return {"head direction": res["hori_rot"] + " " + res["vert_rot"]}
    except Exception as e:
        print(e)
        return {}
