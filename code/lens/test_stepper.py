import os
import sys
import time as og_time

# base_path = os.getcwd()
# sys.path.insert(1, base_path)

from stepper.stepper import Stepper

tele_ring = Stepper(25, 8, 7, 1, 'tele', 300)
focus_ring = Stepper(6, 13, 19, 26, 'focus', 350)

tele_ring.zero_stepper()

# tele_ring.zoom_out(50)
# focus_ring.focus_far(50)

# 350 focus ring
# left (back view) near, right far
# clockwise (left)

# 300 tele
# left (tele), right (wide)
# counterclockwise (left)


