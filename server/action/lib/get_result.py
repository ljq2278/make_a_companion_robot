from utils.path import VISION_DATA


def get_move_result():
    f = open(VISION_DATA, 'r', encoding='utf-8')
    res = [line.strip() for line in f.readlines()]
    return "I have got to a new place. " + ",".join(res) + " in front of me. "

def get_rotate_result():
    f = open(VISION_DATA, 'r', encoding='utf-8')
    res = [line.strip() for line in f.readlines()]
    return "I have changed to a new direction. " + ",".join(res) + " in front of me. "
def get_vision_result():
    f = open(VISION_DATA, 'r', encoding='utf-8')
    res = [line.strip() for line in f.readlines()]
    return "I can see "+",".join(res)
