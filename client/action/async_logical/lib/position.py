import math
from sympy import Point, Circle
import numpy as np

m_speed = 20
r_speed = 90
rot_unit = 45
mv_unit = 20
base_objs = ["Tripod", "Fan", "Monitor/TV"]
base_poses = {"Tripod": [250, 20], "Fan": [0, 0], "Monitor/TV": [40, 200]}


def rela_pos_to_rad(x, y):
    if x == 0:
        x = 0.0001
    deg = np.rad2deg(np.arctan(y / x))
    if y > 0 and x < 0:
        deg = deg + 180
    elif y < 0 and x < 0:
        deg = deg - 180
    # print(x, y, z)
    print(x, y, deg)
    return np.deg2rad(deg)


def get_obj_pos(obj_to_self_rad, obj_dist):
    x = obj_dist * np.cos(obj_to_self_rad)
    y = obj_dist * np.sin(obj_to_self_rad)
    return [x, y]


# def rot_to_get_base(self_stat):
#     rotted = 0
#     base_feat = None
#     while rotted < 360:
#         r_right(rot_unit / r_speed, r_speed)
#         print("rot angle searching base: ", rot_unit)
#         rotted += rot_unit
#         # self_stat["rad"] += np.pi / 3
#         self_stat["rad"] = get_body_direct(use_rad=True)
#         self_stat, features = vision.analysis_vision(self_stat)
#         for feat in features:
#             if feat["cls"] in base_objs:
#                 base_feat = feat
#                 break
#         if base_feat is not None:
#             break
#     print("rot_to_get_base, base_feat: ", base_feat)
#     return base_feat


def adjust_self_feat(self_stat, base_feat):
    real_pos_base = base_poses[base_feat["cls"]]
    real_pos_self = real_pos_base[0] - base_feat["o2s_pos"][0], real_pos_base[1] - base_feat["o2s_pos"][1]
    self_stat["pos"] = real_pos_self
    return self_stat


# def get_self_pos_with_base(rad_to_obj, base_stat, dist):
#     x = base_stat["pos"][0] - dist * np.cos(rad_to_obj)
#     y = base_stat["pos"][1] - dist * np.sin(rad_to_obj)
#     return [x, y]


def get_pos0_by_2dist_1angle_2pos(dist1, dist2, angle, pos1, pos2):
    p1 = Point(pos1[0], pos1[1])
    p2 = Point(pos2[0], pos2[1])
    # Define the circles centered at the known points with radii equal to the distances
    c1 = Circle(p1, dist1)
    c2 = Circle(p2, dist2)
    # Find the intersection points of the circles
    intersections = c1.intersection(c2)
    # Print the coordinates of the intersection points
    for p0 in intersections:
        v1 = [pos1[0] - float(p0.x), pos1[1] - float(p0.y)]
        v2 = [pos2[0] - float(p0.x), pos2[1] - float(p0.y)]
        if v1[0] * v2[1] - v1[1] * v2[0] > 0 and angle < 180:
            return float(p0.x), float(p0.y)
        if v1[0] * v2[1] - v1[1] * v2[0] < 0 and angle >= 180:
            return float(p0.x), float(p0.y)
    return None, None


def get_pos2_by_2dist_1angle_2pos(d10, d20, angle21, pos0, pos1):
    p0 = Point(pos0[0], pos0[1])
    p1 = Point(pos1[0], pos1[1])
    rad21 = math.radians(angle21)
    d21 = math.sqrt(d10 ** 2 + d20 ** 2 - 2 * d10 * d20 * math.cos(rad21))
    # Define the circles centered at the known points with radii equal to the distances
    c0 = Circle(p0, d20)
    c1 = Circle(p1, d21)
    intersections = c0.intersection(c1)
    for p2 in intersections:
        v20 = [pos0[0] - float(p2.x), pos0[1] - float(p2.y)]
        v21 = [pos1[0] - float(p2.x), pos1[1] - float(p2.y)]
        if v20[0] * v21[1] - v20[1] * v21[0] > 0 and angle21 < 180:
            return float(p2.x), float(p2.y)
        if v20[0] * v21[1] - v20[1] * v21[0] < 0 and angle21 >= 180:
            return float(p2.x), float(p2.y)
    return None, None
