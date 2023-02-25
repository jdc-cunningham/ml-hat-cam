import os, pvrhino
from dotenv import load_dotenv
from speech_to_intent.speech_to_intent import RhinoDemo

load_dotenv("/home/pi/ml-hat-cam/code/speech_to_intent/.env")

def zoom_in():
  print("zoom in")

def zoom_out():
  print("zoom out")

def parse_output(output):
  print(output)

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
