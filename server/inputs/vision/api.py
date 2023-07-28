from server_utils.path import VISION_DATA


def get_objs():
    try:
        f = open(VISION_DATA, 'r', encoding='utf-8')
        res = ','.join([line.strip() for line in f.readlines()])
        f.close()
        return res
    except Exception as e:
        print(e)
        return ""
