import os
import sys
import time
import subprocess
# from subprocess import Popen, PIPE, STDOUT

# https://stackoverflow.com/questions/51133407/capture-stdout-and-stderr-of-process-that-runs-an-infinite-loop
# https://stackoverflow.com/questions/803265/getting-realtime-output-using-subprocess

class SpeechIntent():
	def __init__(self, zoom_in_fcn, zoom_out_fcn):
		self.active = False
		self.zoom_in = zoom_in_fcn
		self.zoom_out = zoom_out_fcn

	def start_listening(self):
		self.active = True
		picovoice_ai_key = os.environ.get('picovoice_ai_access_key', os.getcwd())
		cmd = 'picovoice_ai_rhino_mic_demo.py --access_key ' + picovoice_ai_key + ' --context_path Zooming_en_raspberry-pi_v2_1_0.rhn --audio_device_index 1'
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
		
		for line in iter(p.stdout.readline, b''):
			print(line)
			
		p.stdout.close()
		p.wait()