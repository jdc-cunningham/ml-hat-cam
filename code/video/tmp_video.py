from threading import Thread
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
from PIL import Image as im
import time
import cv2 as cv
import numpy as np

class Video:
  def __init__(self, usb_path, focus_stepper):
    self.camera = Picamera2()
    self.encoder = H264Encoder()
    self.record_path = usb_path
    self.focus_stepper = focus_stepper
    self.recording = False
    self.pause_autofocus = False
    # 1080P@60fps
    # 4056, 3040 max lower fps, possibly not possible with rpi
    main_stream_res = {"size": (1280, 720)}
    sample_stream_res = {"size": (640, 480)}
    vid_config = self.camera.create_video_configuration(main_stream_res, sample_stream_res, encode="lores")
    self.camera.configure(vid_config)

  def start_recording(self, file_name):
    self.recording = True
    self.filename = file_name
    self.camera.start_recording(self.encoder, self.record_path + self.filename + '.h264')
    Thread(target=self.start_sampling).start()

  def get_variance(self, np_arr):
    # https://stackoverflow.com/a/32264327/2710227
    pil_img = im.fromarray(np.uint8(np_arr))
    cv_img = cv.cvtColor(np.array(pil_img), cv.COLOR_RGB2BGR)
    var = round(cv.Laplacian(cv_img, cv.CV_64F).var(), 2)
    return var

  def start_sampling(self):
    prev_var = 0

    while self.recording:
      var_samples = []
      focus_far = True # first dir

      if (self.pause_autofocus != True):
        np_arr = self.camera.capture_array("lores")
        variance = self.get_variance(np_arr)
        
        if (prev_var == 0):
          prev_var = variance
          self.focus_stepper.focus_far(25)
        else:
          if (variance > prev_var or variance < 100):
            self.focus_stepper.focus_far(25)
          else:
            self.focus_stepper.focus_near(25)

      print(prev_var)

      prev_var = variance
      time.sleep(0.04) # 24fps

  def stop_recording(self):
    self.recording = False
    self.camera.stop_recording()
