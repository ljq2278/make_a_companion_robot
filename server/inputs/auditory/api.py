from server_utils.path import AUDITORY_DATA


def get_auditory_input():
    try:
        f = open(AUDITORY_DATA, 'r', encoding='utf-8')
        res = [line.strip() for line in f.readlines()][0]
        f.close()
        f = open(AUDITORY_DATA, 'w', encoding='utf-8')
        f.write("")
        f.close()
        return res
    except Exception as e:
        print(e)
        return ""
