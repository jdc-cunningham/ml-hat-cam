import time as og_time
from stepper_motion import *

init_gpio_pins()

def test(steps):
  stepper_clockwise(steps)

og_time.sleep(5)
test(350)


# 350 focus ring
