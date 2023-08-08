from action.physical.move_and_rotate import r_right, r_left, m_up
from action.physical.look import l_init, l_up, vertical_stand_angle
from action.physical.voltage import get_voltage
from action.async_logical.lib import vision
from action.async_logical.lib import position
import numpy as np
import time
from client_utils.others import set_task_state, set_camera_black_mode, set_camera_color_mode, wait_for_static


r_speed_finetune = 60
rot_unit_finetune = 5
mv_last_dist = 35
bias_max_epsilon_factor = 1
align_max_times = 5
try_charge_max_times = 5

def rot_to_center_charge_point(try_time):
    l_init()
    if try_time > align_max_times:
        print("try %s time but not found charge plugin! " % try_time)
        return None, None, None, None
    x, y, sz, bias = vision.get_charge_point()
    rotted = 0
    while x is None:
        r_right(position.rot_unit / position.r_speed, position.r_speed)
        rotted += position.rot_unit
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
    x, y, sz, bias = -1, -1, -1, -1
    while sz < 100:
        x, y, sz, bias = rot_to_center_charge_point(0)
        if sz < 25:
            mv_scale = 10 / sz
            m_up(mv_scale * position.mv_unit / position.m_speed, position.m_speed)
            print("move %f cm toward charge point! " % mv_scale * position.mv_unit)
        elif sz < 35:
            l_up(vertical_stand_angle - 20)
            mv_scale = 10 / sz
            m_up(mv_scale * position.mv_unit / position.m_speed, position.m_speed)
            print("move %f cm toward charge point! " % mv_scale * position.mv_unit)
        else:
            l_init()
            m_up(mv_last_dist / position.m_speed, position.m_speed)
            print("move last %f cm toward charge point! " % mv_last_dist)
            wait_for_static(2)
            if get_voltage() > 7.5:
                return "success"
            else:
                return "failed"
    print("exception x, y, sz, bias: ", x, y, sz, bias)
    return "exception"


def go_charge():
    flg = "exception"
    times = 0
    while flg != "success" and times < try_charge_max_times:
        flg = approach_charge_point()
        times += 1
    return flg


if __name__ == '__main__':
    # print(rot_to_center_charge_point(0))
    set_camera_black_mode()
    exp_res = go_charge()
    set_camera_color_mode()
    if exp_res == "success":
        time.sleep(60 * 60)
        set_task_state("goCharge", "complete", "success")
    else:
        set_task_state("goCharge", "complete", exp_res)
