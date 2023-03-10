# this file is meant to be imported/used externally
# due to the directory imports

import sys
import os
import logging
import time
import traceback

from lib.waveshare_OLED import OLED_1in5_rgb
from PIL import Image, ImageDraw, ImageFont

base_dir = os.getcwd()

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
  'font_1': ImageFont.truetype(base_dir + '/display_menu/pic/Font.ttc', 12),
  'font_2': ImageFont.truetype(base_dir + '/display_menu/pic/Font.ttc', 18),
  'font_3': ImageFont.truetype(base_dir + '/display_menu/pic/Font.ttc', 24)
}

class DisplayMenu():
  def __init__(self):
    self.disp = OLED_1in5_rgb.OLED_1in5_rgb()
    self.text_color = colors['white']
    self.disp.Init()
    self.image = Image.new('RGB', (self.disp.width, self.disp.height), 0)
    self.draw = ImageDraw.Draw(self.image)

  def clear(self):
    self.disp.clear()
    self.image = Image.new('RGB', (self.disp.width, self.disp.height), 0)
    self.draw = ImageDraw.Draw(self.image)

  def clear_battery_status(self):
    self.draw.line([(0, 0), (128, 0)], "BLACK", width = 24)

  def draw_text(self, x, y, text, font = '', color = colors['white']):
    use_font = fonts['font_2']
    if font: use_font = fonts[font]
    self.draw.text((x,y), text, font = use_font, fill = color)
    self.disp.ShowImage(self.disp.getbuffer(self.image))

  def draw_line(self, start_coord, end_coord, fill = colors['white']):
    self.draw.line([(start_coord[0],start_coord[1]),(end_coord[0],end_coord[1])], fill)
    self.disp.ShowImage(self.disp.getbuffer(self.image))
