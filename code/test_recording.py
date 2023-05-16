from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
import time

camera = Picamera2()

encoder = H264Encoder(bitrate=10000000)

camera.resolution = (640, 480)
camera.start_recording(encoder, '/mnt/my_video.h264')
time.sleep(10)

camera.stop_recording()
