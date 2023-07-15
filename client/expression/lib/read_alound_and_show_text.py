import pyttsx3
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import lib.ST7796 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

# Initialize the pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('voice', 'english_rp+f3')

engine.setProperty('rate', 120)  # lower than 200
# Convert the text to speech


# Raspberry Pi configuration.
DC = 21
RST = 22
SPI_PORT = 0
SPI_DEVICE = 0
line_len = 28
font_size = 30
page_lines = 9


def _draw_rotated_text(image, text, position, angle, font, fill=(255, 255, 255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0, 0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=True)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)


def read_alound_and_show_text(txt):
    # Create TFT LCD display class.
    if txt == "":
        txt = "Oop, it seem that I dont know what to say ! "
    disp = TFT.ST7796(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
    # Initialize display.
    disp.begin()
    # Clear the display to a red background.
    # Can pass any tuple of red, green, blue values (from 0 to 255 each).
    # Write two lines of white text on the buffer, rotated 90 degrees counter clockwise.
    font = ImageFont.truetype('assets/Poppins-BoldItalic.ttf', font_size)
    txt_lines_str = ''.join([txt[i] if (i + 1) % line_len != 0 else txt[i] + '\n' for i in range(0, len(txt))])
    txt_lines = txt_lines_str.split('\n')
    for i in range(0, len(txt_lines), page_lines):
        page_txt = '\n'.join(txt_lines[i:i + page_lines])
        disp.clear((0, 0, 0))
        _draw_rotated_text(disp.buffer, page_txt, (0, 10), 90, font, fill=(255, 255, 255))
        disp.display()
        engine.say(''.join(page_txt.split('\n')))

        # Run the engine
        engine.runAndWait()

# read_alound_and_show_text("Here are some ttf font Examples. Here are some ttf font Examples. Here are some ttf font Examples. Here are some ttf font Examples. ")
