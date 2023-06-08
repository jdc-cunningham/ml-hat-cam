from threading import Thread
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
import time
import cv2 as cv
import numpy as np

class Video:
  def __init__(self, usb_path, focus_stepper):
    self.camera = Picamera2()
    self.encoder = H264Encoder()
    self.record_path = usb_path
    self.focus_stepper = focus_stepper
    self.stop_recording = True
    self.pause_autofocus = False
    # 1080P@60fps
    # 4056, 3040 max lower fps, possibly not possible with rpi
    main_stream_res = {"size": (1280, 720)}
    sample_stream_res = {"size": (640, 480)}
    vid_config = self.camera.create_video_configuration(main_stream_res, sample_stream_res, encode="lores")
    self.camera.configure(vid_config)

  def start_recording(self, file_name):
    self.stop_recording = False
    self.filename = file_name
    self.camera.start_recording(self.encoder, self.record_path + self.filename + '.h264', quality=Quality.HIGH)
    Thread(target=self.start_sampling).start()

  def get_variance(self, frame_buffer):
    frame = np.fromstring(frame_buffer, np.uint8)
    img = cv.imdecode(frame, cv.IMREAD_COLOR)
    var = round(cv.Laplacian(img, cv.CV_64F).var(), 2)
    return var

  def start_sampling(self):
    while self.stop_recording != True:
      if (self.pause_autofocus != True):
        frame = self.camera.capture_request()
        variance = self.get_variance(frame)
        print(variance)
      time.sleep(1)

  def stop_recording(self):
    self.stop_recording = True
    self.camera.stop_recording()
