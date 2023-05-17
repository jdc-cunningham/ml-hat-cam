from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
import time

class Video:
  def __init__(self, usb_path):
    self.camera = None
    self.camera = Picamera2()
    self.encoder = H264Encoder(bitrate=10000000)
    # 1080P@60fps
    self.camera.resolution = (1920, 1080) # 4056, 3040 max lower fps, possibly not possible with rpi

  def start_recording(self, file_name):
    self.filename = file_name
    self.camera.start_recording(self.encoder, self.recordpath + self.filename + '.h264')

  def stop_recording(self):
    self.camera.stop_recording()
