import cv2
import requests
import json
import numpy as np
from client_utils.path import VISION_SERVER_IP_PATH, CAMERA_IMG_PATH
from client_utils.others import wait_for_static
# from action.async_logical.lib.combine_action import get_rad_dist
from action.physical.look import l_init, turn_neck
from action.physical.laser import get_dist
from action.async_logical.lib import position
from PIL import Image

# cap_id = 1
show_img_type = "consecutive"
img_height = 480
img_width = 640
scan_cube_size = 5
use_color_channel = 0

y_start = 0
y_end = img_height // 5 * 4
x_start = img_width // 5
x_end = img_width // 5 * 4
bright_thresh = 100

# cap = cv2.VideoCapture(cap_id)
def get_img():
    succ = False
    image = None
    while not succ:
        try:
            image = Image.open(CAMERA_IMG_PATH)
            succ = True
        except Exception as e:
            print(e)
    return image


def get_rad_dist(rad_bias):
    turn_neck(rad_bias)
    return get_dist()


def get_charge_plugin(image):
    data_yx = np.array(image).astype(int)
    # data_yx_diff = np.abs(data_yx[0:-1, 0:-1, :] - data_yx[1:, 1:, :])
    pooled_img = np.zeros([img_height // 5, img_width // 5])
    # y_start = img_height // 3
    for y in range(y_start, y_end, scan_cube_size):
        for x in range(x_start, x_end, scan_cube_size):
            pooled_ind_y = y // scan_cube_size
            pooled_ind_x = x // scan_cube_size
            pooled_img[pooled_ind_y, pooled_ind_x] = np.mean(data_yx[y:y + scan_cube_size, x:x + scan_cube_size, use_color_channel])
            if pooled_img[pooled_ind_y, pooled_ind_x] >= bright_thresh:
                if y > y_start and x > x_start and np.abs(pooled_img[pooled_ind_y, pooled_ind_x] - pooled_img[pooled_ind_y - 1, pooled_ind_x - 1]) > 50:
                    edge_right = pooled_ind_x + 1
                    pooled_img[pooled_ind_y, edge_right] = np.mean(data_yx[y:y + scan_cube_size, edge_right * scan_cube_size:edge_right * scan_cube_size + scan_cube_size, use_color_channel])
                    while pooled_img[pooled_ind_y, edge_right] > pooled_img[pooled_ind_y, pooled_ind_x] - 50 and edge_right < pooled_img.shape[1] - 1:
                        edge_right += 1
                        pooled_img[pooled_ind_y, edge_right] = np.mean(data_yx[y:y + scan_cube_size, edge_right * scan_cube_size:edge_right * scan_cube_size + scan_cube_size, use_color_channel])
                    sz = (edge_right - pooled_ind_x) * scan_cube_size
                    if sz > 40:
                        continue
                    bias = (x + sz + x) / 2 - img_width / 2
                    return x, y, sz, bias
    return None, None, None, None



def get_charge_point():
    wait_for_static(2)
    image = get_img()
    return get_charge_plugin(image)


def get_objs():
    # global cap
    wait_for_static(4)
    # cap.release()
    # cap = cv2.VideoCapture(cap_id)
    # set_camera(cap)
    # ret, frame = cap.read()
    # _, image_encoded = cv2.imencode(".jpg", frame)
    image = get_img()
    _, image_encoded = cv2.imencode(".jpg", np.array(image))
    image_bytes = image_encoded.tobytes()
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    print('get objs from server ...')
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
    obj_to_self_rad = self_stat["rad"] + loc_rad_bias
    dist_nlp = "near" if dist < 50 else "mid" if dist < 200 else "far"
    o2s_pos = position.get_obj_pos(obj_to_self_rad, dist)
    res = {"cls": cls, "loc_rad": loc_rad, "loc_rad_x": xmin, "loc_rad_bias": loc_rad_bias, "o2s_rad": obj_to_self_rad,
           "dist": dist, "dist_nlp": dist_nlp, "o2s_pos": o2s_pos}
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
    resp_objs = get_objs()
    return calc_features(resp_objs, self_stat)


if __name__ == '__main__':
    # print(analysis_vision({"pos": [-150, 150], "rad": -3.14 / 2}))
    print(get_charge_point())
