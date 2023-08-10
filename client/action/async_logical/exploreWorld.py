import sys
sys.path.append(r'/home/pi/Code/client')
# assume that the obj is always filled and obj is always in the vertical plane with the obstacle below.
# and distance meature is aways accurate
from action.physical.say import read_alound_and_show_text
from action.physical.compass import get_body_direct
from action.physical.move_and_rotate import m_up, rotate_to_dest_rad
from action.async_logical.lib import vision
from action.async_logical.lib import position
from client_utils.path import MAP_RECORD_PATH
from client_utils.others import set_task_state
import numpy as np
import json


def random_rotate(self_stat):
    dest_rad = np.random.random() * (2 * np.pi) - np.pi
    rotate_to_dest_rad(dest_rad)
    self_stat["rad"] = dest_rad
    print("random_rotate, dest_rad: ", dest_rad)
    return self_stat


def random_explore(self_stat, mv_speed=position.m_speed, mx_mv_tm=5):
    self_stat = random_rotate(self_stat)
    max_dist_forward = vision.get_rad_dist(0)
    print("random_explore, max_dist_forward: ", max_dist_forward)
    if 10 < max_dist_forward < 1000:
        mv_tm = min(np.random.random() * mx_mv_tm, (max_dist_forward - 4) / mv_speed)
        m_up(mv_tm, mv_speed)
        mv_dist = mv_tm * mv_speed
    else:
        mv_dist = 0
    print("mv_dist: ", mv_dist)
    self_stat["pos"][0] += mv_dist * np.cos(self_stat["rad"])
    self_stat["pos"][1] += mv_dist * np.sin(self_stat["rad"])
    print("random_explore, self_stat: ", self_stat)
    return self_stat


def get_to_new_place_with_base(self_stat):
    self_stat = random_explore(self_stat)
    base_feat = position.rot_to_get_base(self_stat)
    while base_feat is None:
        self_stat = random_explore(self_stat)
        base_feat = position.rot_to_get_base(self_stat)
    print("###################################### find base ################################")
    # here the base_feat is calc according to the self feat. So they should be correct by the real base feat
    self_stat = position.adjust_self_feat(self_stat, base_feat)
    print("get_to_new_place_with_base, self_stat: ", self_stat)
    print("get_to_new_place_with_base, base_feat: ", base_feat)
    return self_stat


def record(features, self_stat):
    print("record: ", features)
    map_record_dict = json.load(open(MAP_RECORD_PATH, 'r', encoding='utf-8'))
    for feat in features:
        if feat["cls"] not in map_record_dict.keys():
            map_record_dict[feat["cls"]] = {}
        view_pos = str(int(self_stat["pos"][0] // 10 * 10)) + "_" + str(int(self_stat["pos"][1] // 10 * 10))
        if view_pos not in map_record_dict[feat["cls"]].keys():
            map_record_dict[feat["cls"]][view_pos] = []
        view_direct = str(int(-np.rad2deg(feat["o2s_rad"]) // 30 * 30))
        if view_direct not in map_record_dict[feat["cls"]][view_pos]:
            map_record_dict[feat["cls"]][view_pos].append(view_direct)
    json.dump(map_record_dict, open(MAP_RECORD_PATH, 'w', encoding='utf-8'))
    return


def one_time_explore(self_stat):
    self_stat = get_to_new_place_with_base(self_stat)
    self_stat = random_rotate(self_stat)
    features = vision.analysis_vision(self_stat=self_stat)
    record(features, self_stat)
    return features, self_stat


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
    try:
        stat = {"pos": [0, 0], "rad": get_body_direct(use_rad=True)}
        feats, s_stat = one_time_explore(stat)
        if len(feats)>0:
            read_alound_and_show_text("I find "+", ".join([feat["cls"] for feat in feats]))
            set_task_state("exploreWorld", "complete", "I find "+", ".join([feat["cls"] for feat in feats]))
        else:
            read_alound_and_show_text("I find nothing new")
            set_task_state("exploreWorld", "complete", "I find nothing new")
        # get_poses_by_base2()
    except Exception as e:
        read_alound_and_show_text("something exception happen when explore the world")
        set_task_state("findObj", "complete", "something exception happen when search the object")