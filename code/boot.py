import os, sys, time

from threading import Thread

lib_dir = os.getcwd() + '/display_menu'
sys.path.append(lib_dir)

from display_menu.display_menu import DisplayMenu
from dpad.dpad import Dpad
from batt_db.batt_db import BattDatabase
from sound.sound import Sound

player = Sound()
batt_db = BattDatabase()
dmenu = DisplayMenu()

def draw_splash_screen():
  dmenu.draw_text(0, 55, 'ML Hat Cam v1')
  dmenu.clear()

def draw_charged_menu():
  dmenu.clear()
  dmenu.draw_text(0, 46, 'Charged?')
  dmenu.draw_text(0, 68, 'Yes')
  dmenu.draw_text(68, 68, 'No', '', 'CYAN')

def highlight_yes():
  dmenu.draw_text(68, 68, 'No', '', 'WHITE')
  dmenu.draw_text(0, 68, 'Yes', '', 'CYAN')

def highlight_no():
  dmenu.draw_text(0, 68, 'Yes', '', 'WHITE')
  dmenu.draw_text(68, 68, 'No', '', 'CYAN')

def draw_batt_status():
  batt_status = batt_db.get_batt_status()
  dmenu.draw_text(0, 0, 'batt: ' + batt_status, 'font_1', 'WHITE')

draw_splash_screen()
time.sleep(3)
draw_charged_menu()
time.sleep(1)
draw_batt_status()

batt_charged = False

def parse_dpad(button_pressed):
  global batt_charged

  if (button_pressed == "LEFT"):
    highlight_yes()
    batt_charged = True

  if (button_pressed == "RIGHT"):
    highlight_no()

  if (button_pressed == "CENTER"):
    if (batt_charged == True):
      batt_db.reset_uptime()
      dmenu.clear()
      draw_batt_status()
    else:
      dmenu.clear()

def poll_battery_status():
  while True:
    draw_batt_status()

    batt_level = batt_db.get_uptime_info()

    if (batt_level[0] >= batt_level[1]):
      player.play_sound_file('sound/files/aws_polly_low-battery.mp3')

    time.sleep(310) # after every 5 minutes

Thread(target=poll_battery_status).start()

control = Dpad(dmenu, parse_dpad)
control.start()
