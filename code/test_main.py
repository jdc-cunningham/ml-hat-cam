from database.database import Database
from usb_storage.usb_storage import UsbStorage
from lens_stepper.lens_stepper import Stepper
from video.tmp_video import Video
import time

db = Database()

focus_ring = Stepper(6, 13, 19, 26, 'focus', 350, db)

usb_storage = UsbStorage()
usb_mounted = usb_storage.check_mounted()

camera = Video('/mnt/', focus_ring)
filename = str(int(time.time()))
camera.start_recording(filename)
time.sleep(5)
camera.stop_recording()