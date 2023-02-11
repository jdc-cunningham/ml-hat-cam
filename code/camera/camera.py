#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

from camera.camera_classes import *
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

output = None

def start_web_stream(focus_ring, tele_ring):
  global output

  picam2 = Picamera2()
  picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
  output = StreamingOutput()
  picam2.start_recording(JpegEncoder(), FileOutput(output))

  try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler(focus_ring, tele_ring))
    server.serve_forever()
  finally:
    picam2.stop_recording()
