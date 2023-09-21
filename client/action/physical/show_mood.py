# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo will fill the screen with white, draw a black box on top
and then print Hello World! in the center of the display

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

from client_utils.path import PRJ_PATH

exp_ent = {
    'norm_e_l': ["￣", (22, 20), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'norm_e_r': ["￣", (76, 20), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'norm_m': ["~", (54, 40), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'hap_e_l': ["^", (28, 20), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'hap_e_r': ["^", (84, 20), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'hap_m': ["︶", (48, 30), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'sad_e_l': ["￣", (22, 20), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'sad_e_r': ["￣", (76, 20), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'sad_m': ["|  へ   |", (32, 24), 20, PRJ_PATH + "assets/STHUPO.TTF"],
    'ama_e_l': ["⊙", (22, 10), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'ama_e_r': ["⊙", (76, 10), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'ama_m': ["o", (56, 20), 35, PRJ_PATH + "assets/Symbola.ttf"],
    'sca_e_l': ["o", (30, 10), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'sca_e_r': ["o", (82, 10), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'sca_m': ["﹏", (47, 12), 35, PRJ_PATH + "assets/Symbola.ttf"],
    'conf_e_l': [".", (30, 5), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'conf_e_r': [".", (82, 5), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'conf_m': ["￣", (50, 40), 24, PRJ_PATH + "assets/STHUPO.TTF"],
    'ang_e_l': ["￣", (22, 24), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'ang_e_r': ["￣", (76, 24), 30, PRJ_PATH + "assets/STHUPO.TTF"],
    'ang_m': ["へ", (56, 32), 20, PRJ_PATH + "assets/STHUPO.TTF"],
}


def _draw_organ(content, drw):
    # drw.text(xy=content[1], text=content[0], font=ImageFont.truetype(font=content[3], size=content[2]), fill=255)
    print(content[0])


def _draw_norm(drw):
    _draw_organ(exp_ent['norm_e_l'], drw)
    _draw_organ(exp_ent['norm_e_r'], drw)
    _draw_organ(exp_ent['norm_m'], drw)


def _draw_confuse(drw):
    _draw_organ(exp_ent['conf_e_l'], drw)
    _draw_organ(exp_ent['conf_e_r'], drw)
    _draw_organ(exp_ent['conf_m'], drw)
    # drw.text(xy=(100, 20), text="?", font=ImageFont.truetype(font=PRJ_PATH + "assets/Symbola.ttf", size=30), fill=255)


def _draw_amaze(drw):
    _draw_organ(exp_ent['ama_e_l'], drw)
    _draw_organ(exp_ent['ama_e_r'], drw)
    _draw_organ(exp_ent['ama_m'], drw)


def _draw_sad(drw):
    _draw_organ(exp_ent['sad_e_l'], drw)
    _draw_organ(exp_ent['sad_e_r'], drw)
    _draw_organ(exp_ent['sad_m'], drw)


def _draw_scared(drw):
    _draw_organ(exp_ent['sca_e_l'], drw)
    _draw_organ(exp_ent['sca_e_r'], drw)
    _draw_organ(exp_ent['sca_m'], drw)


def _draw_ang(drw):
    _draw_organ(exp_ent['ang_e_l'], drw)
    _draw_organ(exp_ent['ang_e_r'], drw)
    _draw_organ(exp_ent['ang_m'], drw)


def _draw_happy(drw):
    _draw_organ(exp_ent['hap_e_l'], drw)
    _draw_organ(exp_ent['hap_e_r'], drw)
    _draw_organ(exp_ent['hap_m'], drw)


def show_mood(txt):
    # Draw a smaller inner rectangle
    print(txt)


if __name__ == '__main__':
    show_mood('sad')
    # show_mood('happy')
