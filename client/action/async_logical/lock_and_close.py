from action.physical.laser import get_dist
from action.physical.look import l_init
from action.physical.move_and_rotate import r_left, r_right, m_up
from action.async_logical.lib.vision import sift_match
import numpy as np

close_dist_thresh = 20


def get_adjust_function(p1):
    if p1 > 1:
        return r_left
    elif p1 < -1:
        return r_right
    else:
        return None


def lock_and_close():
    l_init()
    while get_dist() > close_dist_thresh:
        try:
            p1, p2 = sift_match()
            r_func = get_adjust_function(p1)
            if r_func is not None:
                r_func(np.abs(p1)/10, rot_speed=20)
            m_up(1, mv_speed=20)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    lock_and_close()
