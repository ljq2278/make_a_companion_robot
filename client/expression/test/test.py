# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo will fill the screen with white, draw a black box on top
and then print Hello World! in the center of the display

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


exp_ent = {
    'norm_e_l': ["￣", (22, 20), 30, "STHUPO.TTF"],
    'norm_e_r': ["￣", (76, 20), 30, "STHUPO.TTF"],
    'norm_m': ["~", (54, 40), 30, "STHUPO.TTF"],
    'hap_e_l': ["^", (28, 20), 30, "STHUPO.TTF"],
    'hap_e_r': ["^", (84, 20), 30, "STHUPO.TTF"],
    'hap_m': ["︶", (48, 30), 30, "STHUPO.TTF"],
    'sad_e_l': ["￣", (22, 20), 30, "STHUPO.TTF"],
    'sad_e_r': ["￣", (76, 20), 30, "STHUPO.TTF"],
    'sad_m': ["|  へ   |", (32, 24), 20, "STHUPO.TTF"],
    'ama_e_l': ["⊙", (22, 10), 30, "STHUPO.TTF"],
    'ama_e_r': ["⊙", (76, 10), 30, "STHUPO.TTF"],
    'ama_m': ["o", (56, 20), 35, "Symbola.ttf"],
    'conf_e_l': [".", (30, 5), 30, "STHUPO.TTF"],
    'conf_e_r': [".", (82, 5), 30, "STHUPO.TTF"],
    'conf_m': ["￣", (50, 40), 24, "STHUPO.TTF"],
    'ang_e_l': ["￣", (22, 24), 30, "STHUPO.TTF"],
    'ang_e_r': ["￣", (76, 24), 30, "STHUPO.TTF"],
    'ang_m': ["へ", (56, 32), 20, "STHUPO.TTF"],
}


def draw_organ(content, drw):
    drw.text(xy=content[1], text=content[0], font=ImageFont.truetype(font=content[3], size=content[2]), fill=255)

def draw_norm(drw):
    draw_organ(exp_ent['norm_e_l'], drw)
    draw_organ(exp_ent['norm_e_r'], drw)
    draw_organ(exp_ent['norm_m'], drw)

def draw_confuse(drw):
    draw_organ(exp_ent['conf_e_l'], drw)
    draw_organ(exp_ent['conf_e_r'], drw)
    draw_organ(exp_ent['conf_m'], drw)
    drw.text(xy=(100, 20), text="?", font=ImageFont.truetype(font="Symbola.ttf", size=30), fill=255)

def draw_amaze(drw):
    draw_organ(exp_ent['ama_e_l'], drw)
    draw_organ(exp_ent['ama_e_r'], drw)
    draw_organ(exp_ent['ama_m'], drw)
    drw.text(xy=(110, 20), text="!", font=ImageFont.truetype(font="Symbola.ttf", size=30), fill=255)

def draw_sad(drw):
    draw_organ(exp_ent['sad_e_l'], drw)
    draw_organ(exp_ent['sad_e_r'], drw)
    draw_organ(exp_ent['sad_m'], drw)

def draw_ang(drw):
    draw_organ(exp_ent['ang_e_l'], drw)
    draw_organ(exp_ent['ang_e_r'], drw)
    draw_organ(exp_ent['ang_m'], drw)

def draw_happy(drw):
    draw_organ(exp_ent['hap_e_l'], drw)
    draw_organ(exp_ent['hap_e_r'], drw)
    draw_organ(exp_ent['hap_m'], drw)


def draw_test(drw):
    draw_sad(drw)

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Use for SPI
# spi = board.SPI()
# oled_cs = digitalio.DigitalInOut(board.D5)
# oled_dc = digitalio.DigitalInOut(board.D6)
# oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# # Load default font.
# font = ImageFont.load_default()
#
# # Draw Some Text
# text = "Hello World!"
# (font_width, font_height) = font.getsize(text)

draw_test(draw)
# draw.text(
#     (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
#     text,
#     font=font,
#     fill=255,
# )

# Display image
oled.image(image)
oled.show()
