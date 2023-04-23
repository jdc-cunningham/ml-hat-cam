import os, pvrhino
from database.database import Database
from lens_stepper.stepper import Stepper
from camera.camera import start_web_stream
from dotenv import load_dotenv
from speech_to_intent.speech_to_intent import RhinoDemo
from threading import Thread
from sound.sound import Sound

player = Sound()

load_dotenv(os.getcwd() + "/speech_to_intent/.env")

db = Database()

focus_ring = Stepper(6, 13, 19, 26, 'focus', 350, db)
tele_ring = Stepper(12, 16, 20, 21, 'tele', 300, db)

def start_camera():
  start_web_stream(focus_ring, tele_ring)

def zoom_in():
  print("zoom in")

def zoom_out():
  print("zoom out")

zoom_level = 1 # 1, 2, 3 = close, middle, far

# zoom for wideopen
focus_ring.focus_far(320)

def parse_output(output):
  global zoom_level

  # tele vs. zoom
  # 0, 320
  # 150, 210
  # 300, 0

  if (output == 'ZoomIn' and zoom_level < 4):
    zoom_level += 1
    tele_pos = tele_ring.get_pos()

    if (tele_pos == 0): # to 150
      tele_ring.zoom_in(150)
      focus_ring.focus_near(120)
      player.play_sound_file('sound/files/aws_polly_medium-zoom.mp3')

    if (tele_pos == 150): # to 300
      tele_ring.zoom_in(150)
      focus_ring.focus_near(120) # get to 220
      player.play_sound_file('sound/files/aws_polly_max-zoom.mp3')

  if (output == 'ZoomOut' and zoom_level > 0):
    zoom_level -= 1
    tele_pos = tele_ring.get_pos()

    if (tele_pos == 300): # to 150
      tele_ring.zoom_out(150)
      focus_ring.focus_far(210)
      player.play_sound_file('sound/files/aws_polly_medium-zoom.mp3')

    if (tele_pos == 150): # to 0
      tele_ring.zoom_out(150)
      focus_ring.focus_far(110)
      player.play_sound_file('sound/files/aws_polly_wide-open.mp3')

def start_voice_listening():
  picovoice_ai_key = os.getenv('PV_AI_ACCESS_KEY')

  speechIntent = RhinoDemo(
    access_key=picovoice_ai_key,
    library_path=pvrhino.LIBRARY_PATH,
    model_path=pvrhino.MODEL_PATH,
    context_path=os.getcwd() + '/speech_to_intent/Zooming_en_raspberry-pi_v2_1_0.rhn',
    endpoint_duration_sec=1,
    require_endpoint=False,
    audio_device_index=1,
    output_path=None,
    output_callback=parse_output
  ).run()

Thread(target=start_voice_listening).start()
start_camera()