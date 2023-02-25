import os
import sys
import time
from subprocess import Popen, PIPE, STDOUT

# https://stackoverflow.com/questions/51133407/capture-stdout-and-stderr-of-process-that-runs-an-infinite-loop


class SpeechIntent():
	def __init__(self, zoom_in_fcn, zoom_out_fcn):
		self.active = False
		self.zoom_in = zoom_in_fcn
		self.zoom_out = zoom_out_fcn

	def start_listening(self):
		self.active = True
		picovoice_ai_key = os.environ.get('picovoice_ai_access_key', os.getcwd())
		cmd_string = 'rhino_demo_mic --access_key ' + picovoice_ai_key + ' --context_path Zooming_en_raspberry-pi_v2_1_0.rhn --audio_device_index 1'
		args = (sys.executable, '-u', cmd_string)
		cmd = ' '.join(args)
		p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, universal_newlines=True)

    lines = iter(p.stdout.readline, '')
    for line in lines:
      line = line.rstrip()
      print(line)

		# while (self.active):
			# lines = (p.stdout.readline, '')
			# print(lines)
			# line = lines[len(lines) - 1]
			# line = line.rstrip()
			# print(line.rstrip())
			# time.sleep(0.5)

    # for line in iter(p.stdout.readline,''):
      # line = line.rstrip()
      # print(line)
