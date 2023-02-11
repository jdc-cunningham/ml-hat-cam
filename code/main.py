from database.database import Database
from lens_stepper.stepper import Stepper

output = None # nasty

from camera.camera import start_web_stream

db = Database()

focus_ring = Stepper(6, 13, 19, 26, 'focus', 350, db)
tele_ring = Stepper(12, 16, 20, 21, 'tele', 300, db)

start_web_stream(focus_ring, tele_ring)
