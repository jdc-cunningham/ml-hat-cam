import os, sys, time

from threading import Thread

lib_dir = os.getcwd() + '/display_menu'
sys.path.append(lib_dir)

from display_menu.display_menu import DisplayMenu
from dpad.dpad import Dpad
from batt_db.batt_db import BattDatabase
from sound.sound import Sound
from utils.utils import Utils
from usb_storage.usb_storage import UsbStorage
from mic.mic import Mic
from video.video import Video

player = Sound()
batt_db = BattDatabase()
dmenu = DisplayMenu() # 128 x 128
utils = Utils()

usb_storage = UsbStorage()
usb_mounted = usb_storage.check_mounted()

if (not usb_mounted):
  # force USB usage so SD card lasts longer
  dmenu.draw_text(0, 55, 'No USB drive')
  sys.exit("USB not mounted")

record_state = {
  'recording': False,
  'zoom_level': 'near',
  'active_menu': 'recording',
  'video': Video('/mnt'),
  'audio': Mic('/mnt')
}

batt_checked = False

def check_recording_state(button_press):
  global record_state

  if (record_state['active_menu'] == 'recording'):
    if (button_press == 'CENTER'):
      record_state['recording'] = not record_state['recording']

      if (record_state['recording']):
        filename = time()
        record_state['audio'].start_recording(filename)
        record_state['video'].start_recording(filename)
      else:
        record_state['audio'].stop_recording(filename)
        record_state['video'].stop_recording(filename)

    if (button_press == 'DOWN'):
      record_state['active_menu'] = 'zoom_level'

  # these will not require a second click eg. CENTER just changing activates it
  if (record_state['active_menu'] == 'zoom_level'):
    cur_zoom = record_state['zoom_level']

    if (button_press == 'LEFT'): # this should be an easy array cycle
      if (cur_zoom != 'near'):
        if (cur_zoom == 'far'):
          record_state['zoom_level'] = 'mid'
        else:
          record_state['zoom_level'] = 'near'

    if (button_press == 'RIGHT'):
      if (cur_zoom != 'far'):
        if (cur_zoom == 'near'):
          record_state['zoom_level'] = 'mid'
        else:
          record_state['zoom_level'] = 'far'
    
    if (button_press == 'UP'):
      record_state['active_menu'] = 'recording'

  dmenu.clear()
  draw_recording_state()
  draw_zoom_state()


def draw_splash_screen():
  dmenu.draw_text(0, 55, 'ML Hat Cam v1')
  dmenu.draw_text(0, 75, 'ip: ' + utils.get_ip(), 'font_1')
  time.sleep(3)
  dmenu.clear()

def draw_charged_menu():
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
  dmenu.clear_battery_status()
  dmenu.draw_text(0, 0, 'batt: ' + batt_status, 'font_1', 'WHITE')

def draw_recording_state():
  record_row_active = record_state['active_menu'] == 'recording'

  if (record_state['recording']):
    dmenu.draw_text(0, 48, 'Stop recording', '', 'CYAN' if record_row_active else 'WHITE')
  else:
    dmenu.draw_text(0, 48, 'Start recording', '', 'CYAN' if record_row_active else 'WHITE')

def draw_zoom_state():
  zoom_row_active = record_state['active_menu'] == 'zoom_level'

  if (record_state['zoom_level'] == 'near'):
    dmenu.draw_text(0, 68, 'near', '', 'CYAN' if zoom_row_active else 'WHITE')
    dmenu.draw_text(55, 68, 'mid', '', 'WHITE')
    dmenu.draw_text(100, 68, 'far', '', 'WHITE')
  elif (record_state['zoom_level'] == 'mid'):
    dmenu.draw_text(0, 68, 'near', '', 'WHITE')
    dmenu.draw_text(55, 68, 'mid', '', 'CYAN' if zoom_row_active else 'WHITE')
    dmenu.draw_text(100, 68, 'far', '', 'WHITE')
  else:
    dmenu.draw_text(0, 68, 'near', '', 'WHITE')
    dmenu.draw_text(55, 68, 'mid', '', 'WHITE')
    dmenu.draw_text(100, 68, 'far', '', 'CYAN' if zoom_row_active else 'WHITE')

draw_splash_screen()
time.sleep(3)
draw_charged_menu()
draw_batt_status()

batt_charged = False

def parse_dpad(button_pressed):
  global batt_charged, batt_checked

  if batt_checked:
    check_recording_state(button_pressed)
  else:
    if (button_pressed == "LEFT"):
      highlight_yes()
      batt_charged = True

    if (button_pressed == "RIGHT"):
      highlight_no()

    if (button_pressed == "CENTER"):
      if (batt_charged == True):
        batt_db.reset_uptime()
        dmenu.clear()
      else:
        dmenu.clear()

      batt_checked = True

      draw_batt_status()
      draw_recording_state()
      draw_zoom_state()

def poll_battery_status():
  while True:
    draw_batt_status()

    batt_level = batt_db.get_uptime_info()

    if (batt_level[0] >= batt_level[1]):
      player.play_sound_file('sound/files/aws_polly_low-battery.mp3')

    # time.sleep(60)
    # time.sleep(310) # after every 5 minutes

# turn this off for now
# Thread(target=poll_battery_status).start()

control = Dpad(dmenu, parse_dpad)
control.start()
