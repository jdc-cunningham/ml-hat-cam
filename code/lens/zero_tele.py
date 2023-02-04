import time as og_time

from stepper.stepper import Stepper

tele_ring = Stepper(12, 16, 20, 21, 'tele', 300)

tele_ring.zero_stepper()
