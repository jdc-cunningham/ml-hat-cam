#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import io
import shutil
import logging
import time
from threading import Condition, Thread

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

while True:
  with output.condition:
      output.condition.wait()
      frame = output.frame
  
  with open('vid.mjpeg', 'wb') as file:
      shutil.copyfileobj(frame, file)

  # self.wfile.write(b'--FRAME\r\n')
  # self.send_header('Content-Type', 'image/jpeg')
  # self.send_header('Content-Length', len(frame))
  # self.end_headers()
  # self.wfile.write(frame)
  # self.wfile.write(b'\r\n')

  time.sleep(5)
  break

picam2.stop_recording()