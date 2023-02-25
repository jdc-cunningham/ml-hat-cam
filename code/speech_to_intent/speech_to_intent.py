import os
import sys
import time
import subprocess
from subprocess import Popen, PIPE, STDOUT

import pvrhino
from picovoice_ai_rhino_mic_demo import RhinoDemo

# https://stackoverflow.com/questions/51133407/capture-stdout-and-stderr-of-process-that-runs-an-infinite-loop
# https://stackoverflow.com/questions/803265/getting-realtime-output-using-subprocess

class SpeechIntent():
	def __init__(self, zoom_in_fcn, zoom_out_fcn):
		self.active = False
		self.zoom_in = zoom_in_fcn
		self.zoom_out = zoom_out_fcn
		
	def parse_output(self, output):
		print(output)

	def start_listening(self):
		picovoice_ai_key = os.environ.get('picovoice_ai_access_key', os.getcwd())

		RhinoDemo(
      access_key=picovoice_ai_key,
      library_path=pvrhino.LIBRARY_PATH,
      model_path=pvrhino.MODEL_PATH,
      context_path='Zooming_en_raspberry-pi_v2_1_0.rhn',
      endpoint_duration_sec=1,
      require_endpoint=False,
      audio_device_index=1,
      output_path=None,
      output_callback=self.parse_output
    ).run()