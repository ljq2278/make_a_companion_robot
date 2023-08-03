# assume that the obj is always filled and obj is always in the vertical plane with the obstacle below.
# and ultrasound is aways accurate

from action.physical.move_and_rotate import r_right, m_up
from action.async_logical.lib import vision

import numpy as np


base_objs = ["Tripod", "Fan", "Monitor/TV"]
base_poses = {"Tripod": [-100, 300], "Fan": [0, 0], "Monitor/TV": [-200, 0]}
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
        r_right(rot_unit / r_speed)
        print("rot angle searching base: ", rot_unit)
        rotted += rot_unit
        self_stat["rad"] += np.pi / 3
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


def get_to_new_place_with_base(self_stat):
    self_stat = random_explore(self_stat)
    base_feat = rot_to_get_base(self_stat)
    while base_feat is None:
        self_stat = random_explore(self_stat)
        base_feat = rot_to_get_base(self_stat)
    print("get_to_new_place_with_base, self_stat: ", self_stat)
    print("get_to_new_place_with_base, base_feat: ", base_feat)
    return self_stat


def record(features):
    print("record: ", features)
    return


def one_time_explore(self_stat):
    self_stat = get_to_new_place_with_base(self_stat)
    self_stat = random_rotate(self_stat)
    features = vision.analysis_vision(self_stat=self_stat)
    record(features)
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
    stat = {"pos": [-150, 150], "rad": -3.14 / 2}
    one_time_explore(stat)
    # get_poses_by_base2()
