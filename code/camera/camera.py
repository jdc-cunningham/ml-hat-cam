#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import io
import logging
import socketserver
import cv2 as cv
import numpy as np

from http import server
from threading import Condition, Thread
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

output = None
focus_ring = None
tele_ring = None
prev_var = 0
next_var = 0
max_var = 0
dir_near = None

PAGE = """\
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
  def __init__(self):
    self.frame = None
    self.condition = Condition()

  def write(self, buf):
    with self.condition:
      self.frame = buf
      self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
  def get_variance(self, frame_buffer):
    img = cv.imdecode(frame_buffer, cv.IMREAD_COLOR)
    return round(cv.Laplacian(img, cv.CV_64F).var(), 2)

  # - get the first current value
  # - find which direction increases next values
  # - find max value, stop
  def check_focus(self, frame_buffer):
    global prev_var, next_var, max_var, dir_near

    step_size = 25

    if (prev_var == 0):
      prev_var = self.get_variance(frame_buffer)
      max_var = prev_var
      # rotate in advance for next value
      focus_ring.focus_near(step_size)
      return

    # get second sample
    if (next_var == 0):
      next_var = self.get_variance(frame_buffer)

      if (next_var > max_var):
        max_var = next_var
        return
    else: # decide direction to keep going
      if (next_var > prev_var):
        dir_near = True
        focus_ring.focus_near(step_size)
      else:
        dir_near = False
        focus_ring.focus_far(step_size)
      return

    if (dir_near):
      cur_var = self.get_variance(frame_buffer)
    else:
      cur_var = self.get_variance(frame_buffer)
    
    # find max value and stop
    if (cur_var):
      if (cur_var > max_var):
        max_var = cur_var
      elif (cur_var <= max_var):
        return

  def do_GET(self):
    global focus_ring, tele_ring, frame_counter, prev_var, var_largest, focused_far, best_focus_reached

    if self.path == '/':
      self.send_response(301)
      self.send_header('Location', '/index.html')
      self.end_headers()
    elif self.path == '/index.html':
      content = PAGE.encode('utf-8')
      self.send_response(200)
      self.send_header('Content-Type', 'text/html')
      self.send_header('Content-Length', len(content))
      self.end_headers()
      self.wfile.write(content)
    elif self.path == '/stream.mjpg':
      self.send_response(200)
      self.send_header('Age', 0)
      self.send_header('Cache-Control', 'no-cache, private')
      self.send_header('Pragma', 'no-cache')
      self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
      self.end_headers()

      try:
        while True:
          with output.condition:
            output.condition.wait()
            frame = output.frame

          self.wfile.write(b'--FRAME\r\n')
          self.send_header('Content-Type', 'image/jpeg')
          self.send_header('Content-Length', len(frame))
          self.end_headers()
          self.wfile.write(frame)
          self.wfile.write(b'\r\n')

          self.check_focus(frame)

      except Exception as e:
        logging.warning(
          'Removed streaming client %s: %s',
          self.client_address, str(e))
    else:
      self.send_error(404)
      self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
  allow_reuse_address = True
  daemon_threads = True

def start_web_stream(fr, tr):
  global output, focus_ring, tele_ring

  focus_ring = fr
  tele_ring = tr

  picam2 = Picamera2()
  picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
  output = StreamingOutput()
  picam2.start_recording(JpegEncoder(), FileOutput(output))

  try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
  finally:
    picam2.stop_recording()
