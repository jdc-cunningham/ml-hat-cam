
import os
import sys
import time as og_time

from database.database import Database
from lens.stepper.stepper import Stepper

db = Database()

focus_ring = Stepper(6, 13, 19, 26, 'focus', 350, db)
tele_ring = Stepper(12, 16, 20, 21, 'tele', 300, db)

def set_manual_values(pos):
  focus_ring.cur_pos = pos
  tele_ring.cur_pos = pos

  focus_ring.update_stepper_db_pos(pos)
  tele_ring.update_stepper_db_pos(pos)
  exit()

# set_manual_values(0)

# back view looking to front of camera
# tele - right (wide)
# focus - right (far)


# tele_ring.zero_stepper()
# tele_ring.zero_stepper_manual()

# focus_ring.zero_stepper()
# focus_ring.zero_stepper_manual()

# tele_ring.zoom_out(250)
# focus_ring.focus_far(50)
# focus_ring.focus_near(50)

# 350 focus ring
# left (back view) near, right far
# clockwise (left)

# 300 tele
# left (tele), right (wide)
# counterclockwise (left)


