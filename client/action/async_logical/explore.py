from action.physical.move_and_rotate import r_left, r_right, m_up
from action.physical.ultrasound_measure import ur_disMeasure
from action.physical.look import ur_disMeasure
import numpy as np
import time


def explore(ttm):
    mv_speed = 20
    rot_speed = 90
    mx_mv_tm = 5
    start_tm = int(time.time())
    while int(time.time()) - start_tm < ttm:
        rot_func = r_left if np.random.random() < 0.5 else r_right
        rot_tm = np.random.random() * 2
        rot_func(rot_tm, rot_speed)
        max_dist_forward = np.mean([ur_disMeasure() for _ in range(0, 10)])
        print("max_dist_forward: ", max_dist_forward)
        if max_dist_forward > 15:
            mv_tm = min(np.random.random() * mx_mv_tm, max_dist_forward / mv_speed)
            print("mv_tm: ", mv_tm)
            m_up(mv_tm, mv_speed)


if __name__ == '__main__':
    explore(30)
