import time as og_time
from stepper_motion import *

init_gpio_pins()

def rotate(steps):
  stepper_clockwise(steps)
  # stepper_counter_clockwise(steps)

og_time.sleep(5)

rotate(350)


# 350 focus ring
# left (back view) near, right far
# clockwise (left)

# 300 tele
# left (tele), right (wide)
# counterclockwise (left)
