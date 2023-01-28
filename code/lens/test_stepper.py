import time as og_time
from stepper_motion import *
from steper_motion_2 import *

init_gpio_pins()

def rotate(steps):
  stepper_clockwise(steps)

og_time.sleep(5)

test(50)


# 350 focus ring
