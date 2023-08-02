# assume that the obj is always filled and obj is always in the vertical plane with the obstacle below.
# and ultrasound is aways accurate

from action.physical.move_and_rotate import r_right, m_up
from action.async_logical.lib import vision

import requests
import numpy as np
from sympy import Point, Circle
import cv2
import json
import math

base_objs = ["Tripod", "Fan", "Monitor/TV"]
base_poses = {"Tripod": [-100, 300], "Fan": [0, 0], "Monitor/TV": [-200, 0]}
m_speed = 20
r_speed = 90


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
        r_right(0.2)
        rotted += 60
        self_stat["rad"] += np.pi / 3
        resp_objs = vision.get_objs()
        features = vision.calc_features(resp_objs, self_stat)
        for feat in features:
            if feat["cls"] in base_objs:
                base_feat = feat
                break
        if base_feat is not None:
            break
    print("base_feat: ", base_feat)
    return base_feat


# def rot_to_get_base_from_base(base_cls):
#     rotted = 0
#     found = False
#     rot_funcs = [r_right, r_left]
#     direct = None
#     new_base = None
#     dist = -1
#     sz = -1
#     for i, rot_fun in enumerate(rot_funcs):
#         while rotted < 180:
#             rot_fun(0.2)
#             rotted += 60
#             resp_objs = vision.get_objs()
#             features = vision.calc_features(resp_objs, np.deg2rad(rotted))
#             for feat in features:
#                 if feat["cls"] != base_cls and feat["cls"] in base_objs:
#                     found = True
#                     new_base = feat["cls"]
#                     dist = feat["dist"]
#                     direct = "right" if i == 0 else "left"
#                     break
#             if found:
#                 break
#         if found:
#             break
#         else:
#             rot_funcs[1 - i](2)
#             rotted = 0
#     print("new_base, direct, rotted, dist, sz: ", new_base, direct, rotted, dist, sz)
#     return new_base, direct, rotted, dist, sz
#
#
# def see_base2():
#     base1, dist1, sz1 = rot_to_get_base()
#     if base1 is not None:
#         base2, direct, rotted, dist2, sz2 = rot_to_get_base_from_base(base1)
#         if base2 is not None:
#             return True, rotted if direct == "left" else 360 - rotted, dist1, dist2, base1, base2, sz1, sz2
#     return False, None, None, None, None, None, None, None


def random_explore(self_stat, rot_speed=r_speed, mv_speed=m_speed, mx_mv_tm=5):
    rot_tm = np.random.random() * 4
    r_right(rot_tm, rot_speed)
    rot_angle = rot_tm * rot_speed
    print("rot_angle: ", rot_angle)
    max_dist_forward = vision.get_rad_dist(0)
    print("max_dist_forward: ", max_dist_forward)
    if 10 < max_dist_forward < 1000:
        mv_tm = min(np.random.random() * mx_mv_tm, (max_dist_forward - 4) / mv_speed)
        m_up(mv_tm, mv_speed)
        mv_dist = mv_tm * mv_speed
    else:
        mv_dist = 0
    print("mv_dist: ", mv_dist)
    self_stat["rad"] += np.deg2rad(rot_angle)
    self_stat["pos"][0] += mv_dist * np.cos(self_stat["rad"])
    self_stat["pos"][1] += mv_dist * np.sin(self_stat["rad"])
    return self_stat


def get_to_new_place_with_base(self_stat):
    self_stat = random_explore(self_stat)
    base_feat = rot_to_get_base(self_stat)
    while base_feat is None:
        self_stat = random_explore(self_stat)
        base_feat = rot_to_get_base(self_stat)
    print("self_stat: ", self_stat)
    print("base_feat: ", base_feat)
    return self_stat


# def get_to_new_place_with_base2():
#     global obj_pos
#     random_explore()
#     succ, angle, dist1, dist2, cls1, cls2, sz1, sz2 = see_base2()
#     while not succ:
#         random_explore()
#         succ, angle, dist1, dist2, cls1, cls2, sz1, sz2 = see_base2()
#     self_pos = position.get_pos0_by_2dist_1angle_2pos(dist1, dist2, angle, obj_pos[cls1], obj_pos[cls2])
#     print("I am at ", self_pos)
#     return self_pos

def record(features):
    print(features)
    return


def one_time_explore(self_stat):
    new_self_stat = get_to_new_place_with_base(self_stat)
    features = vision.analysis_vision(self_stat=new_self_stat)
    feats_with_global_pos = []
    for feat in features:
        feat["pos"][0] += new_self_stat["pos"][0]
        feat["pos"][1] += new_self_stat["pos"][1]
        feats_with_global_pos.append(feat)
    record(feats_with_global_pos)
    return new_self_stat


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
    stat = {"pos": [-150, 150], "rad": -3.14 / 2}
    one_time_explore(stat)
    # get_poses_by_base2()
