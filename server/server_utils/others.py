import time


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
