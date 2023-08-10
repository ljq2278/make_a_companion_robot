import sys
sys.path.append(r'/home/pi/Code/client')
from action.physical.move_and_rotate import r_right, r_left, m_up
from action.physical.say import read_alound_and_show_text
from action.async_logical.lib import vision
from action.async_logical.lib import position
import numpy as np
from client_utils.others import set_task_state


def find_person():
    rotted = 0
    while rotted < 360:
        r_right(position.rot_unit / position.r_speed, position.r_speed)
        rotted += position.rot_unit
        resp_objs = vision.get_objs()
        for resp_obj in resp_objs:
            if resp_obj["name"] == "Person":
                return True
    return False


if __name__ == '__main__':
    # print(rot_to_center_charge_point(0))
    try:
        words = sys.argv[1]
        print(words)
        found = find_person()
        if found:
            read_alound_and_show_text(words)
            set_task_state("findPersonChat", "complete", "success, it's in front of you")
        else:
            read_alound_and_show_text("where is the person?")
            set_task_state("findPersonChat", "complete", "failed, can not find a person")
    except Exception as e:
        print(e)
        set_task_state("findPersonChat", "complete", "something exception happen when searching a person")
#
# if __name__ == '__main__':
#     # print(rot_to_center_charge_point(0))
#     try:
#         words = sys.argv[1]
#         print(words)
#         read_alound_and_show_text(words)
#         set_task_state("findPersonChat", "complete", "success")
#     except Exception as e:
#         print(e)
#         set_task_state("findPersonChat", "complete", "something exception happen when searching a person")

