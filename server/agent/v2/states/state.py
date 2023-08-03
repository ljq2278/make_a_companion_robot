from inputs.vision.api import get_objs
from inputs.keyboard.api import get_keyboard_input
from inputs.others.api import get_others_dict
from inputs.body.api import get_body


def get_states():
    res = get_others_dict()
    res.update(get_body())
    res.update(
        {
            "head vision": get_objs(),
        }
    )
    res.update(
        {
            "human message": get_keyboard_input(),
        }
    )
    return res
