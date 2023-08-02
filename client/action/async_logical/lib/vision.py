import cv2
import requests
import json
import numpy as np
from client_utils.path import VISION_SERVER_IP_PATH
from client_utils.others import wait_for_static, set_camera
# from action.async_logical.lib.combine_action import get_rad_dist
from action.physical.look import l_init, turn_neck
from action.physical.ultrasound_measure import get_dist
from action.async_logical.lib import position

show_img_type = "consecutive"
cap = cv2.VideoCapture(0)


def get_rad_dist(rad_bias):
    turn_neck(rad_bias)
    return get_dist()


def get_objs():
    global cap
    wait_for_static(1)
    cap.release()
    cap = cv2.VideoCapture(0)
    set_camera(cap)
    ret, frame = cap.read()
    _, image_encoded = cv2.imencode(".jpg", frame)
    image_bytes = image_encoded.tobytes()
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    print('get objs ...')
    response = requests.post(VISION_SERVER_IP_PATH, files=files, data={'text': show_img_type})
    if response.status_code == 200:
        print('get objs success ')
        return json.loads(response.text)
    else:
        print('get objs failed ')
        return []


def calc_feature(resp_obj, self_stat):
    cls = resp_obj["name"]
    xmin, ymin, xmax, ymax = resp_obj["bbox"]
    xmin_rad = xmin * (1 / 3 * np.pi)
    xmax_rad = xmax * (1 / 3 * np.pi)
    loc_rad = xmax_rad - xmin_rad
    cent_loc_rad = (xmin_rad + xmax_rad) / 2
    loc_rad_bias = cent_loc_rad - 1 / 6 * np.pi
    dist = get_rad_dist(loc_rad_bias)
    global_center_rad = self_stat["rad"] + loc_rad_bias
    dist_nlp = "near" if dist < 50 else "mid" if dist < 200 else "far"
    pos = position.get_obj_pos(self_stat, dist)
    res = {"cls": cls, "loc_rad": loc_rad, "loc_rad_x": xmin, "loc_rad_bias": loc_rad_bias, "rad": global_center_rad,
           "dist": dist, "dist_nlp": dist_nlp, "pos": pos}
    print("calc_feature: ", res)
    return res


def calc_features(resp_objs, self_stat):
    features = []
    for itm in resp_objs:
        features.append(calc_feature(itm, self_stat))
    return features


# def get_obj_feature(cap, cls, self_rad):
#     # return the most center one
#     res = None
#     resp_objs = get_objs(cap)
#     for itm in resp_objs:
#         if itm["name"] == cls:
#             tmp = calc_feature(itm, self_rad)
#             if res is None:
#                 res = tmp
#             elif np.abs(tmp["rad_bias"]) < np.abs(res["rad_bias"]):
#                 res = tmp
#     return res
#
#
# def rot_to_align_and_get_dist(cap, obj_feat, self_rad, r_speed=90):
#     # dist from rad center(60/2/180*np.pi)
#     while np.abs(obj_feat["rad_bias"]) > 0.1:
#         adust_rad = -obj_feat["rad_bias"]
#         rot_func = r_right if adust_rad > 0 else r_left
#         rot_func(np.rad2deg(adust_rad) / r_speed)
#         get_obj_feature(cap, obj_feat["cls"], self_rad)
#     return get_forward_dist()


# def get_obj_dist_with_retreat_look(rad, conf_rad, confirm_dist):
#     # rad*dist = conf_rad*(dist+confirm_dist)
#     dist = conf_rad * confirm_dist / (rad - conf_rad)
#     return dist, dist * rad


def analysis_vision(self_stat):
    global cap
    resp_objs = get_objs()
    return calc_features(resp_objs, self_stat)


if __name__ == '__main__':
    print(analysis_vision({"rad": 0}))
    # print(get_rad_dist(-0.4))
