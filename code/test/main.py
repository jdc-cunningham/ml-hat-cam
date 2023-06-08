from usb_storage import UsbStorage
from video import Video
import time

usb_storage = UsbStorage()
usb_mounted = usb_storage.check_mounted()

focus_ring = None

camera = Video('/mnt/', focus_ring)
camera.start_recording()
time.sleep(5)
camera.stop_recording()
