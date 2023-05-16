from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
import time

class Video:
  def __init__(self, usb_path):
    self.camera = None
    self.recordpath = usb_path

  def start_recording(self, file_name):
    self.filename = file_name
    self.camera = Picamera2()
    encoder = H264Encoder(bitrate=10000000)
    self.camera.resolution = (640, 480)
    self.camera.start_recording(encoder, self.recordpath + self.filename + '.h264')
    time.sleep(21600)

  def stop_recording(self):
    self.camera.stop_recording()