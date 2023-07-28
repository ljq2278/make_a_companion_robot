from inputs.vision.api import get_objs
from inputs.keyboard.api import get_keyboard_input
from inputs.kernel.api import get_kernel_data
from inputs.ultrasound.api import get_obst_dist
from inputs.body.api import get_body


def get_states():
    res = dict(get_kernel_data())
    res.update(get_body())
    res.update(
        {
            "head vision": get_objs(),
        }
    )
    res.update(
        {
            "obstacle ahead": "true" if get_obst_dist() < 10 else "false",
        }
    )
    res.update(
        {
            "human message": get_keyboard_input(),
        }
    )

    return res
