from usb_storage import UsbStorage
from stepper import Stepper
from video import Video
import time

usb_storage = UsbStorage()
usb_mounted = usb_storage.check_mounted()

focus_ring = None

camera = Video('/mnt/', focus_ring)
filename = str(int(time.time()))
camera.start_recording(filename)
time.sleep(5)
camera.stop_recording()
