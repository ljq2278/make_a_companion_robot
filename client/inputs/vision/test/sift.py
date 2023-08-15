import sys

sys.path.append(r'/home/pi/Code/client')
import numpy as np
import cv2 as cv
import time
from client_utils.path import CAMERA_IMG_PATH

img0_path = CAMERA_IMG_PATH
img1_path = "/".join(CAMERA_IMG_PATH.split("/")[:-1]) + "/test.png"


#####################################################

def match():
    cur_time = str(int(time.time()))
    img0 = cv.imread(img0_path, cv.IMREAD_GRAYSCALE)
    img1 = cv.imread(img1_path, cv.IMREAD_GRAYSCALE)

    # 初始化 AKAZE 探测器
    akaze = cv.AKAZE_create()
    # 使用 SIFT 查找关键点和描述
    kp0, des0 = akaze.detectAndCompute(img0, None)
    cv.imwrite(r"Figure0_keypoint.png", cv.drawKeypoints(img0, kp0, img0))
    kp1, des1 = akaze.detectAndCompute(img1, None)
    cv.imwrite(r"Figure1_keypoint.png", cv.drawKeypoints(img1, kp1, img1))

    # BFMatcher 默认参数
    bf = cv.BFMatcher()
    matches = bf.knnMatch(des0, des1, k=2)

    # 旋转测试
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append([m])
    # good_matches = matches
    # 画匹配点
    img2 = cv.drawMatchesKnn(img0, kp0, img1, kp1, good_matches, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv.imwrite("/".join(CAMERA_IMG_PATH.split("/")[:-1]) + '/matches_%s.jpg' % cur_time, img2)

    # 选择匹配关键点
    img0_kpts = np.float32([kp0[m[0].queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    img1_kpts = np.float32([kp1[m[0].trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # 计算 homography
    H, status = cv.findHomography(img0_kpts, img1_kpts, cv.RANSAC, 5.0)
    print("trans matrix: ", H)
    # 变换
    warped_image = cv.warpPerspective(img0, H, (img0.shape[1] + img1.shape[1], img0.shape[0] + img1.shape[0]))

    cv.imwrite("/".join(CAMERA_IMG_PATH.split("/")[:-1]) + '/warped_%s.jpg' % cur_time, warped_image)


if __name__ == '__main__':
    while True:
        match()
        time.sleep(1)
