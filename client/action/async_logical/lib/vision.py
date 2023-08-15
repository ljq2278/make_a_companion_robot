import sys

sys.path.append(r'/home/pi/Code/client')
import cv2
import requests
import json
import numpy as np
from client_utils.path import VISION_SERVER_IP_PATH, CAMERA_IMG_PATH, PREV_IMG_PATH, MAP_RECORD_PATH
from client_utils.others import wait_for_static
from action.physical.compass import get_body_direct
# from action.async_logical.lib.combine_action import get_rad_dist
from action.physical.look import l_init, turn_neck
from action.physical.move_and_rotate import rotate_to_dest_rad
from action.physical.laser import get_dist
from action.async_logical.lib import position
from PIL import Image
import time
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

#
# def set_camera(cap):
#     cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
#     print("CAP_PROP_BRIGHTNESS: ", cap.get(cv2.CAP_PROP_BRIGHTNESS))
#     cap.set(cv2.CAP_PROP_CONTRAST, 32)  # 对比度 32
#     print("CAP_PROP_CONTRAST: ", cap.get(cv2.CAP_PROP_CONTRAST))
#     cap.set(cv2.CAP_PROP_SATURATION, 64)  # 饱和度 64
#     print("CAP_PROP_SATURATION: ", cap.get(cv2.CAP_PROP_SATURATION))
#     cap.set(cv2.CAP_PROP_HUE, 0)  # 色调 0
#     cap.set(cv2.CAP_PROP_EXPOSURE, -4)  # 曝光 -4
#     return
#
# cap_id = 0
# # cap_id += + cv2.CAP_DSHOW
# cap1 = cv2.VideoCapture(cap_id)
# # os.system("bash ~/camera.sh")
# set_camera(cap1)
# # subprocess.Popen(["/usr/bin/uvcdynctrl", " -d /dev/video1 -S 6:10 '(LE)0x0400'"])
# # time.sleep(1)
# send_frame_rate = 24
# pre_camera_img = None


def get_img():
    succ = False
    image = None
    while not succ:
        try:
            time.sleep(0.5)
            image = Image.open(CAMERA_IMG_PATH)
            succ = True
        except Exception as e:
            print(e)
    return image


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


def record(self_stat, features):
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


def get_objs():
    # global cap
    wait_for_static(2)
    image = get_img()
    # ret, image = cap1.read()
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


def calc_feature(self_state, resp_obj):
    cls = resp_obj["name"]
    xmin, ymin, xmax, ymax = resp_obj["bbox"]
    xmin_rad = xmin * (1 / 3 * np.pi)
    xmax_rad = xmax * (1 / 3 * np.pi)
    loc_rad = xmax_rad - xmin_rad
    cent_loc_rad = (xmin_rad + xmax_rad) / 2
    loc_rad_bias = cent_loc_rad - 1 / 6 * np.pi
    turn_neck(loc_rad_bias)
    dist = get_dist()
    obj_to_self_rad = get_body_direct(True) + loc_rad_bias
    dist_nlp = "near" if dist < 50 else "mid" if dist < 200 else "far"
    o2s_pos = position.get_obj_pos(obj_to_self_rad, dist)
    res = {"cls": cls, "loc_rad": loc_rad, "loc_rad_x": xmin, "loc_rad_bias": loc_rad_bias, "o2s_rad": obj_to_self_rad,
           "dist": dist, "dist_nlp": dist_nlp, "o2s_pos": o2s_pos}
    print("calc_feature: ", res)
    if cls in position.base_objs:
        print("find base onj! ", res)
        self_state = position.adjust_self_feat(self_state, res)
    return self_state, res


def calc_features(self_state, resp_objs):
    features = []
    base_obj_exist = False
    for itm in resp_objs:
        if itm["name"] in position.base_objs:
            base_obj_exist = True
        self_state, obj_feat = calc_feature(self_state, itm)
        features.append(obj_feat)
    if base_obj_exist:
        record(self_state, features)
    return self_state, features


def analysis_vision(self_state):
    tt_features = []
    for dest_rad in [-3.14, -2.36, -1.57, -0.78, 0, 0.78, 1.57, 2.36]:
        rotate_to_dest_rad(dest_rad)
        resp_objs = get_objs()
        self_state, features = calc_features(self_state, resp_objs)
        tt_features += features
    return self_state, tt_features


# def update_view_brightness(self_state):
#     image = get_img()
#     # image = None
#     # while image is None:
#     #     ret, image = cap1.read()
#     self_state["view_brt"] = np.mean(image)
#     return self_state


def sift_match(img0_path=CAMERA_IMG_PATH, img1_path=PREV_IMG_PATH):
    # cur_time = str(int(time.time()))
    img0 = cv2.imread(img0_path, cv2.IMREAD_GRAYSCALE)
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)

    # 初始化 AKAZE 探测器
    akaze = cv2.AKAZE_create()
    # 使用 SIFT 查找关键点和描述
    kp0, des0 = akaze.detectAndCompute(img0, None)
    # cv2.imwrite(r"Figure0_keypoint.png", cv2.drawKeypoints(img0, kp0, img0))
    kp1, des1 = akaze.detectAndCompute(img1, None)
    # cv2.imwrite(r"Figure1_keypoint.png", cv2.drawKeypoints(img1, kp1, img1))

    # BFMatcher 默认参数
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des0, des1, k=2)

    # good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append([m])
    # good_matches = matches
    # 画匹配点
    # img2 = cv2.drawMatchesKnn(img0, kp0, img1, kp1, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # cv2.imwrite("/".join(CAMERA_IMG_PATH.split("/")[:-1]) + '/matches_%s.jpg' % cur_time, img2)

    # 选择匹配关键点
    img0_kpts = np.float32([kp0[m[0].queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    img1_kpts = np.float32([kp1[m[0].trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # 计算 homography
    H, status = cv2.findHomography(img0_kpts, img1_kpts, cv2.RANSAC, 5.0)
    print("trans matrix: \n", H, "\n")
    # 变换
    # warped_image = cv2.warpPerspective(img0, H, (img0.shape[1] + img1.shape[1], img0.shape[0] + img1.shape[0]))
    #
    # cv2.imwrite("/".join(CAMERA_IMG_PATH.split("/")[:-1]) + '/warped_%s.jpg' % cur_time, warped_image)
    return H[0, 2], H[1, 2]


if __name__ == '__main__':
    # print(analysis_vision({"pos": [-150, 150], "rad": -3.14 / 2}))
    # print(get_charge_point())
    # print(sift_match())
    # while cap1.isOpened():
    print(update_view_brightness({}))
