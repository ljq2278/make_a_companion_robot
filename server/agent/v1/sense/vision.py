from server.utils.path import VISION_ACTION_RESULT_FILE


def get_seeing():
    res = set()
    f_obj = open(VISION_ACTION_RESULT_FILE, 'r', encoding='utf-8')
    for line in f_obj.readlines():
        res.add(line.strip())
    f_obj.close()
    return ",".join(list(res))
