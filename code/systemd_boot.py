import os, sys, time

from threading import Thread

lib_dir = os.getcwd() + '/display_menu'
sys.path.append(lib_dir)

from display_menu.display_menu import DisplayMenu
from dpad.dpad import Dpad
from batt_db.batt_db import BattDatabase
from database.database import Database
from lens_stepper.stepper import Stepper
from sound.sound import Sound
from utils.utils import Utils
from usb_storage.usb_storage import UsbStorage
from mic.mic import Mic
from video.video import Video

player = Sound()
batt_db = BattDatabase()
dmenu = DisplayMenu() # 128 x 128
utils = Utils()
video = Video('/mnt/')
video_thread = None # oof
mic = Mic('/mnt/')
mic_thread = None
db = Database()

focus_ring = Stepper(6, 13, 19, 26, 'focus', 350, db)
tele_ring = Stepper(12, 16, 20, 21, 'tele', 300, db)

# set to near focus
focus_ring.focus_far(330)
tele_ring.zoom_out(0) # should be at 0 already, autozero's on boot

usb_storage = UsbStorage()
usb_mounted = usb_storage.check_mounted()

if (not usb_mounted):
  # force USB usage so SD card lasts longer
  dmenu.draw_text(0, 55, 'No USB drive')
  sys.exit("USB not mounted")

record_state = {
  'recording': False,
  'zoom_level': 'near',
  'active_menu': 'recording'
}

batt_checked = False

def check_recording_state(button_press):
  global record_state, video_thread, audio_thread

  if (record_state['active_menu'] == 'recording'):
    if (button_press == 'CENTER'):
      record_state['recording'] = not record_state['recording']

      if (record_state['recording']):
        filename = str(int(time.time()))
        audio_thread = Thread(target=mic.start_recording, args=(filename,))
        audio_thread.start()
        # mic.start_recording(filename)
        video_thread = Thread(target=video.start_recording, args=(filename,))
        video_thread.start()
      else:
        video.stop_recording()
        mic.stop = True

    if (button_press == 'DOWN'):
      record_state['active_menu'] = 'zoom_level'

  # these will not require a second click eg. CENTER just changing activates it
  if (record_state['active_menu'] == 'zoom_level'):
    cur_zoom = record_state['zoom_level']

    if (button_press == 'LEFT'): # this should be an easy array cycle
      if (cur_zoom != 'near'):
        if (cur_zoom == 'far'):
          record_state['zoom_level'] = 'mid'
          focus_ring.focus_far(140)
          tele_ring.zoom_out(150)
        else:
          record_state['zoom_level'] = 'near'
          focus_ring.focus_far(120)
          tele_ring.zoom_out(150)

    if (button_press == 'RIGHT'):
      if (cur_zoom != 'far'):
        if (cur_zoom == 'near'):
          record_state['zoom_level'] = 'mid'
          focus_ring.focus_near(120)
          tele_ring.zoom_in(150)
        else:
          record_state['zoom_level'] = 'far'
          focus_ring.focus_near(140)
          tele_ring.zoom_in(150)
    
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
