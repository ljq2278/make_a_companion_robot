import sys

sys.path.append(r'/home/pi/Code/client')
# assume that the obj is always filled and obj is always in the vertical plane with the obstacle below.
# and distance meature is aways accurate
from action.physical.say import read_alound_and_show_text
from action.physical.move_and_rotate import m_up_photic, rotate_to_dest_rad
from action.physical.look import l_init
from action.async_logical.lib import vision
from action.async_logical.lib import position
from client_utils.others import set_task_state, wait_for_static
import numpy as np


mv_tm_unit = 2
min_view_brightness = 80
# rot_speed = 80

def random_rotate():
    dest_rad = np.random.random() * (2 * np.pi) - np.pi
    print("random_rotate, dest_rad: ", dest_rad, " start")
    rotate_to_dest_rad(dest_rad)
    wait_for_static(2)
    return

def random_explore(self_state, mv_speed=position.m_speed):
    l_init()
    print("start rotate ...")
    random_rotate()
    print("start moving ...")
    m_up_photic(mv_tm_unit, mv_speed)
    print("start analysis vision ...")
    self_state, features = vision.analysis_vision(self_state)
    return self_state, features

# def random_explore(self_state, mv_speed=position.m_speed):
#     l_init()
#     random_rotate()
#     # self_state = vision.update_view_brightness(self_state)
#     print(self_state)
#     while self_state["view_brt"] < min_view_brightness:
#         random_rotate()
#         # self_state = vision.update_view_brightness(self_state)
#         print(self_state)
#     print("start moving ...")
#     m_up(mv_tm_unit, mv_speed)
#     print("start analysis vision ...")
#     self_state, features = vision.analysis_vision(self_state)
#     return self_state, features


# def get_to_new_place_with_base(self_stat):
#     random_explore()
#     base_feat = position.rot_to_get_base(self_stat)
#     while base_feat is None:
#         random_explore()
#         base_feat = position.rot_to_get_base(self_stat)
#     print("###################################### find base ################################")
#     # here the base_feat is calc according to the self feat. So they should be correct by the real base feat
#     self_stat = state.update_self_state(self_stat, base_feat)
#     print("get_to_new_place_with_base, self_stat: ", self_stat)
#     print("get_to_new_place_with_base, base_feat: ", base_feat)
#     return self_stat


if __name__ == '__main__':
    # explore(30)
    # m_up(1,mv_speed=10)
    # r_left(1)
    # r_right(0.2)
    # calc_feature()
    # print(rot_to_get_base())
    # print(rot_to_get_base_from_base('Fan'))
    # calc_feature()
    # calc_feature()
    # calc_feature()
    # ang = 90
    # print(get_pos0_by_2dist_1angle_2pos(5, 5, ang, [0, 0], [5, 5]))
    # print(get_pos2_by_2dist_1angle_2pos(5, 5, ang, [0, 5], [0, 0]))
    while True:
        try:
            s_stat, feats = random_explore({})
            if len(feats) > 0:
                read_alound_and_show_text("I find " + ", ".join([feat["cls"] for feat in feats]))
                set_task_state("exploreWorld", "complete", "I find " + ", ".join([feat["cls"] for feat in feats]))
            else:
                read_alound_and_show_text("I find nothing new")
                set_task_state("exploreWorld", "complete", "I find nothing new")
            # get_poses_by_base2()
        except Exception as e:
            print(e)
            read_alound_and_show_text("something exception happen when explore the world")
            set_task_state("findObj", "complete", "something exception happen when search the object")
