from utils.path import VISION_DATA


def get_vision_result():
    f = open(VISION_DATA, 'r', encoding='utf-8')
    res = [line.strip() for line in f.readlines()]
    return "I can see "+",".join(res)
