import sys
sys.path.append(r'/home/pi/Code/client')

from action.physical.move_and_rotate import r_right, r_left, m_up, rotate_to_dest_rad
from action.physical.say import read_alound_and_show_text
from action.physical.compass import get_body_direct
from client_utils.others import set_task_state
from action.async_logical.lib import position
import numpy as np
from client_utils.path import MAP_RECORD_PATH
import json
import sys


def get_obj_info(nm):
    while True:
        try:
            objs_info = json.load(open(MAP_RECORD_PATH, 'r', encoding='utf-8'))
            break
        except Exception as e:
            print(e)
    if nm in objs_info.keys():
        return objs_info[nm]
    else:
        return None


def get_2pos_dist(pos0, pos1):
    return np.sqrt(np.square(pos0[0] - pos1[0]) + np.square(pos0[1] - pos1[1]))


def go_to_pos(self_stat, pos):
    base_feat = position.rot_to_get_base(self_stat)
    self_stat = state.update_self_state(self_stat, base_feat)
    dest_rad = position.rela_pos_to_rad(pos[0] - self_stat["pos"][0], pos[1] - self_stat["pos"][1])
    rotate_to_dest_rad(dest_rad)
    mv_dist = get_2pos_dist(pos, self_stat["pos"])
    m_up(mv_dist / position.m_speed, position.m_speed)


if __name__ == '__main__':
    # print(rot_to_center_charge_point(0))
    try:
        obj_info = get_obj_info(sys.argv[1])
        if obj_info is not None:
            go_to_pos({"pos": [0, 0], "rad": get_body_direct()}, [int(t) for t in list(obj_info.keys())[0].split('_')])
            rotate_to_dest_rad(int(obj_info[list(obj_info.keys())[0]][0]))
            read_alound_and_show_text("find dest obj! ")
            set_task_state("findObj", "complete", "success, it's in front of you")
        else:
            read_alound_and_show_text("find obj failed! ")
            set_task_state("findObj", "complete", "failed, can not find it")
    except Exception as e:
        print(e)
        set_task_state("findObj", "complete", "something exception happen when search the object")