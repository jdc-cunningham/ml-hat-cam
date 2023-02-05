from database.database import Database
from lens.stepper.stepper import Stepper

db = Database()

focus_ring = Stepper(6, 13, 19, 26, 'focus', 350, db)
tele_ring = Stepper(12, 16, 20, 21, 'tele', 300, db)

print("init pos")
print(focus_ring.get_pos())

focus_ring.focus_far(50)

print(focus.ring.get_pos())
