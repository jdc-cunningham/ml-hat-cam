import sys
import os

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging    
import time
import traceback
from waveshare_OLED import OLED_1in5_rgb
from PIL import Image,ImageDraw,ImageFont
logging.basicConfig(level=logging.DEBUG)

try:
    disp = OLED_1in5_rgb.OLED_1in5_rgb()

    logging.info("\r 1.5inch rgb OLED ")
    # Initialize library.
    disp.Init()
    # Clear display.
    logging.info("clear display")
    disp.clear()

    # Create blank image for drawing.
    image1 = Image.new('RGB', (disp.width, disp.height), 0)
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font2 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    logging.info ("***draw line")
    draw.line([(0,0),(127,0)], fill = "RED")
    draw.line([(0,0),(0,127)], fill = "RED")
    draw.line([(0,127),(127,127)], fill = "RED")
    draw.line([(127,0),(127,127)], fill = "RED")
    logging.info ("***draw text")
    draw.text((20,0), 'Waveshare ', font = font1, fill = "BLUE")
    draw.text((20,24), u'微雪电子 ', font = font2, fill = "MAGENTA")
    draw.text((20,64), 'Waveshare ', font = font1, fill = "CYAN")
    draw.text((20,92), u'微雪电子 ', font = font2, fill = "GREEN")
    image1 = image1.rotate(0)
    disp.ShowImage(disp.getbuffer(image1))
    time.sleep(3)

    logging.info ("***draw rectangle")
    image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image1)
    draw.line([(0,8), (127,8)],   fill = "RED",    width = 16)
    draw.line([(0,24),(127,24)],  fill = "YELLOW", width = 16)
    draw.line([(0,40),(127,40)],  fill = "GREEN",  width = 16)
    draw.line([(0,56),(127,56)],  fill = "CYAN",   width = 16)
    draw.line([(0,72),(127,72)],  fill = "BLUE",   width = 16)
    draw.line([(0,88),(127,88)],  fill = "MAGENTA",width = 16)
    draw.line([(0,104),(127,104)],fill = "BLACK",  width = 16)
    draw.line([(0,120),(127,120)],fill = "WHITE",  width = 16)
    disp.ShowImage(disp.getbuffer(image1))
    time.sleep(3)

    disp.clear()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    OLED_1in5_rgb.config.module_exit()
    exit()

