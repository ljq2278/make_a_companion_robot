import sys

sys.path.append(r'/home/pi/Code/client')
# assume that the obj is always filled and obj is always in the vertical plane with the obstacle below.
# and distance meature is aways accurate
from action.physical.say import read_alound_and_show_text
from action.physical.move_and_rotate import m_up, m_up_photic, rotate_to_dest_rad
from action.physical.look import l_init
from action.async_logical.lib import vision
from action.async_logical.lib import position
from client_utils.others import set_task_state, wait_for_static
import numpy as np

m_speed = 20
r_speed = 90
rot_unit = 45
mv_unit = 20
mv_tm_unit = 5
min_view_brightness = 80


# rot_speed = 80

def random_rotate():
    dest_rad = np.random.random() * (2 * np.pi) - np.pi
    print("random_rotate, dest_rad: ", dest_rad, " start")
    rotate_to_dest_rad(dest_rad)
    wait_for_static(2)
    return


def random_explore(self_state):
    l_init()
    print("start rotate ...")
    random_rotate()
    print("start moving ...")
    success = m_up_photic(mv_tm_unit)
    while not success:
        print("start rotate ...")
        random_rotate()
        print("start moving ...")
        success = m_up_photic(mv_tm_unit)
    print("start analysis vision ...")
    self_state, features = vision.analysis_vision(self_state)
    return self_state, features


if __name__ == '__main__':

    while True:
        try:
            s_stat, feats = random_explore({})
            if len(feats) > 0:
                read_alound_and_show_text("I find " + ", ".join([feat["cls"] for feat in feats]))
                set_task_state("exploreWorld", "complete", "I find " + ", ".join([feat["cls"] for feat in feats]))
            else:
                read_alound_and_show_text("I find nothing new")
                set_task_state("exploreWorld", "complete", "I find nothing new")
            # get_poses_by_base2()
        except Exception as e:
            print(e)
            read_alound_and_show_text("something exception happen when explore the world")
            set_task_state("findObj", "complete", "something exception happen when search the object")
