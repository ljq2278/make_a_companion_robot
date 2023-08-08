from action.physical.move_and_rotate import r_right, r_left, m_up
from action.physical.look import l_init, l_up, vertical_stand_angle
from action.async_logical.lib import vision
import numpy as np

m_speed = 20
r_speed = 90
r_speed_finetune = 60
mv_unit = 10
rot_unit = 30
rot_unit_finetune = 5
mv_last_dist = 35
bias_max_epsilon_factor = 1


def rot_to_center_charge_point(try_time):
    if try_time > 5:
        print("try %s time but not found charge plugin! " % try_time)
        return None, None, None, None
    # l_init()
    x, y, sz, bias = vision.get_charge_point()
    rotted = 0
    while x is None:
        r_right(rot_unit / r_speed, r_speed)
        rotted += rot_unit
        x, y, sz, bias = vision.get_charge_point()
    print("found charge point! x, y, sz, bias: ", x, y, sz, bias)
    try:
        while np.abs(bias) > bias_max_epsilon_factor * sz:  # bias with far away can be a little much
            rot_func = r_left if bias < -bias_max_epsilon_factor * sz else r_right
            rot_func(rot_unit_finetune / r_speed_finetune, r_speed_finetune)
            x, y, sz, bias = vision.get_charge_point()
            print("x, y, sz, bias: ", x, y, sz, bias)
        return x, y, sz, bias
    except Exception as e:
        print(e)
        return rot_to_center_charge_point(try_time + 1)


def approach_charge_point():
    l_init()
    x, y, sz, bias = -1, -1, -1, -1
    while sz < 100:
        x, y, sz, bias = rot_to_center_charge_point(0)
        if sz < 25:
            mv_scale = 10 / sz
            m_up(mv_scale * mv_unit / m_speed, m_speed)
            print("move %f cm toward charge point! " % mv_scale * mv_unit)
        elif sz < 35:
            l_up(vertical_stand_angle - 20)
            mv_scale = 10 / sz
            m_up(mv_scale * mv_unit / m_speed, m_speed)
            print("move %f cm toward charge point! " % mv_scale * mv_unit)
        # elif sz < 40:
        #     l_up(vertical_stand_angle - 40)
        #     mv_scale = 10 / sz
        #     m_up(mv_scale * mv_unit / m_speed, m_speed)
        #     print("move %f cm toward charge point! " % mv_scale * mv_unit)
        else:
            l_init()
            m_up(mv_last_dist / m_speed, m_speed)
            print("move last %f cm toward charge point! " % mv_last_dist)
            return "end"
    print("exception x, y, sz, bias: ", x, y, sz, bias)
    return "exception"


if __name__ == '__main__':
    # print(rot_to_center_charge_point(0))
    print(approach_charge_point())
