# assume that the obj is always filled and obj is always in the vertical plane with the obstacle below.
# and ultrasound is aways accurate

from action.physical.compass import get_body_direct
from action.physical.move_and_rotate import r_right, m_up
from action.async_logical.lib import vision
from client_utils.path import MAP_RECORD_PATH
from client_utils.others import set_task_state
import numpy as np
import json

base_objs = ["Tripod", "Fan", "Monitor/TV"]
base_poses = {"Tripod": [250, 20], "Fan": [0, 0], "Monitor/TV": [40, 200]}
m_speed = 20
r_speed = 90
rot_unit = 60


#############
# self_stat = {
#     "pos": [-50, 50],
#     "rad": 0,
# }
#############


def rot_to_get_base(self_stat):
    rotted = 0
    base_feat = None
    while rotted < 360:
        r_right(rot_unit / r_speed, r_speed)
        print("rot angle searching base: ", rot_unit)
        rotted += rot_unit
        # self_stat["rad"] += np.pi / 3
        self_stat["rad"] = get_body_direct(use_rad=True)
        features = vision.analysis_vision(self_stat)
        for feat in features:
            if feat["cls"] in base_objs:
                base_feat = feat
                break
        if base_feat is not None:
            break
    print("rot_to_get_base, base_feat: ", base_feat)
    return base_feat


def random_rotate(self_stat, rot_speed=r_speed):
    rot_tm = np.random.random() * 4
    r_right(rot_tm, rot_speed)
    rot_angle = rot_tm * rot_speed
    self_stat["rad"] += np.deg2rad(rot_angle)
    print("random_rotate, rot_angle: ", rot_angle)
    return self_stat


def random_explore(self_stat, rot_speed=r_speed, mv_speed=m_speed, mx_mv_tm=5):
    self_stat = random_rotate(self_stat, rot_speed)
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


def adjust_self_feat(self_stat, base_feat):
    real_pos_base = base_poses[base_feat["cls"]]
    real_pos_self = real_pos_base[0] - base_feat["o2s_pos"][0], real_pos_base[1] - base_feat["o2s_pos"][1]
    self_stat["pos"] = real_pos_self
    return self_stat


def get_to_new_place_with_base(self_stat):
    self_stat = random_explore(self_stat)
    base_feat = rot_to_get_base(self_stat)
    while base_feat is None:
        self_stat = random_explore(self_stat)
        base_feat = rot_to_get_base(self_stat)
    # here the base_feat is calc according to the self feat. So they should be correct by the real base feat
    self_stat = adjust_self_feat(self_stat, base_feat)
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
            map_record_dict[feat["cls"]][view_pos] = set()
        view_direct = str(int(-np.rad2deg(feat["o2s_rad"]) // 30 * 30))
        map_record_dict[feat["cls"]][view_pos].add(view_direct)
    json.dump(map_record_dict, open(MAP_RECORD_PATH, 'w', encoding='utf-8'))
    return


def one_time_explore(self_stat):
    self_stat = get_to_new_place_with_base(self_stat)
    self_stat = random_rotate(self_stat)
    features = vision.analysis_vision(self_stat=self_stat)
    record(features, self_stat)
    return self_stat


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
    stat = {"pos": [-150, 150], "rad": get_body_direct(use_rad=True)}
    res = one_time_explore(stat)
    set_task_state("exploreWorld", "complete", res)
    # get_poses_by_base2()
