from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
import time

class Video:
  def __init__(self, usb_path):
    self.camera = None
    self.camera = Picamera2()
    self.encoder = H264Encoder(bitrate=10000000)
    self.record_path = usb_path
    # 1080P@60fps
    # 4056, 3040 max lower fps, possibly not possible with rpi
    self.camera.create_video_configuration()

  def start_recording(self, file_name):
    self.filename = file_name
    self.camera.start_recording(self.encoder, self.record_path + self.filename + '.h264', Quality.HIGH)

  def stop_recording(self):
    self.camera.stop_recording()
