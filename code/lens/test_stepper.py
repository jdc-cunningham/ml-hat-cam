import os
import sys
import time as og_time

from stepper.stepper import Stepper

focus_ring = Stepper(6, 13, 19, 26, 'focus', 350)
tele_ring = Stepper(12, 16, 20, 21, 'tele', 300)

# back view looking to front of camera
# tele - right (wide)
# focus - right (far)


# tele_ring.zero_stepper()
# focus_ring.zero_stepper()

# tele_ring.zoom_out(250)
# focus_ring.focus_far(50)

# 350 focus ring
# left (back view) near, right far
# clockwise (left)

# 300 tele
# left (tele), right (wide)
# counterclockwise (left)


