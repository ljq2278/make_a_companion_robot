from server_utils.path import ULTRASOUND_DATA


def get_obst_dist():
    try:
        f = open(ULTRASOUND_DATA, 'r', encoding='utf-8')
        res = [line.strip() for line in f.readlines()][0]
        f.close()
        return int(res)
    except Exception as e:
        print(e)
        return 1
