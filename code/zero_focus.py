import time as og_time

from stepper.stepper import Stepper

focus_ring = Stepper(6, 13, 19, 26, 'focus', 350)

focus_ring.zero_stepper()
