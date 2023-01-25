from stepper_motion import *

init_gpio_pins()

def test(steps):
  stepper_clockwise(steps)

test(512)

