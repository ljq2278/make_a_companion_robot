from server.utils.path import VISION_DATA


def get_seeing():
    res = set()
    f_obj = open(VISION_DATA, 'r', encoding='utf-8')
    for line in f_obj.readlines():
        res.add(line.strip())
    f_obj.close()
    return ",".join(list(res))
