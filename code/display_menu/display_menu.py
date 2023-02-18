import sys
import os

picdir = os.getcwd() + '/pic'
libdir = os.getcwd() + '/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging    
import time
import traceback
from waveshare_OLED import OLED_1in5_rgb
from PIL import Image,ImageDraw,ImageFont
logging.basicConfig(level=logging.DEBUG)

colors = {
  'red': 'RED',
  'yellow': 'YELLOW',
  'green': 'GREEN',
  'cyan': 'CYAN',
  'blue': 'BLUE',
  'magenta': 'MAGENTA',
  'black': 'BLACK',
  'white': 'WHITE'
}

fonts = {
  'font_1': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12),
  'font_2': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18),
  'font_3': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
}

class DisplayMenu():
  def __init__(self):
    disp = OLED_1in5_rgb.OLED_1in5_rgb()
    disp.Init()
    disp.clear()
    self.text_color = colors.white

  def draw_text(self, x, y, text, font = fonts.font_1, color = self.text_color):
    draw.text((x,y), text, font, color)
    disp.ShowImage(disp.getbuffer(image1))

  def draw_line(self, start_coord, end_coord, color = self.text_color):
    draw.line([(start_coord[0],start_coord[1]),(end_coord[0],end_coord[1])], color)
    disp.ShowImage(disp.getbuffer(image1))
