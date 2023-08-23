from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import lib.ST7796 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from client_utils.path import PRJ_PATH

# Raspberry Pi configuration.
DC = 16
RST = 13
SPI_PORT = 0
SPI_DEVICE = 0
font_size = 40
width = 480
height = 320
cur_posi = [0, 0]

disp = TFT.ST7796(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
# Initialize display.
disp.begin()


def _draw_rotated_text(image, text, position, angle, font, fill=(255, 255, 255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)

    textdraw.text((0, 0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=True)
    # Paste the text into the image, using it as a mask for transparency.

    image.paste(rotated, (position[1], width - position[0] - font_size // 2))


def _clear(image, position, fill=(0, 0, 0)):
    draw = ImageDraw.Draw(image)
    x0, y0, x1, y1 = position[1], width - position[0], position[1] + font_size, width - position[0] - font_size // 2
    if x0 > x1:
        tmp = x0
        x0 = x1
        x1 = tmp
    if y0 > y1:
        tmp = y0
        y0 = y1
        y1 = tmp
    draw.rectangle((x0, y0, x1, y1), outline=255, fill=fill)


def draw_text(s):
    global cur_posi
    # Create TFT LCD display class.

    if s != "" and (cur_posi[0] < width and cur_posi[1] < height):
        _draw_rotated_text(disp.buffer, s, cur_posi, 90, ImageFont.truetype(font=PRJ_PATH + "assets/STHUPO.TTF", size=font_size))
        if cur_posi[0] >= width - font_size // 2:
            cur_posi[0] = 0
            cur_posi[1] += font_size
        else:
            cur_posi[0] += font_size // 2
    elif s == "" and (cur_posi[0] > 0 or cur_posi[1] > 0):
        if cur_posi[0] <= 0:
            cur_posi[0] = width - font_size // 2
            cur_posi[1] -= font_size
        else:
            cur_posi[0] -= font_size // 2
        _clear(disp.buffer, cur_posi)
    disp.display()


def clear_text(fill=(0, 0, 0)):
    global cur_posi
    draw = ImageDraw.Draw(disp.buffer)
    draw.rectangle((0, 0, height, width), outline=255, fill=fill)
    disp.display()
    cur_posi[0] = cur_posi[1] = 0


if __name__ == '__main__':
    draw_text("s")
