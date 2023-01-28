# based on
# https://github.com/custom-build-robots/Stepper-motor-28BYJ-48-Raspberry-Pi/blob/master/decision-maker.py

from time import sleep
import RPi.GPIO as GPIO

class Stepper:
  def __init__(self, pin1, pin2, pin3, pin4, name, max_pos):
    IN1 = pin1
    IN2 = pin2
    IN3 = pin3
    IN4 = pin4

    step_wait_time = 0.001
    name = name
    min_pos = 0 # assumes calibrated at max stop one side
    max_pos = max
    cur_pos = 0

    self.init_gpio_pins()

  def update_cur_pos(self, step):
    if self.cur_pos < step:
      self.cur_pos = self.cur_pos - 1
    else:
      self.cur_pos = self.cur_pos + 1

  def init_gpio_pins(self):
    # set GPIO pins
    GPIO.setup(self.IN1,GPIO.OUT)
    GPIO.setup(self.IN2,GPIO.OUT)
    GPIO.setup(self.IN3,GPIO.OUT)
    GPIO.setup(self.IN4,GPIO.OUT)

    # set pins to false
    GPIO.output(self.IN1, False)
    GPIO.output(self.IN2, False)
    GPIO.output(self.IN3, False)
    GPIO.output(self.IN4, False)

  def step_1(self):
      GPIO.output(self.IN4, True)
      sleep (self.time)
      GPIO.output(self.IN4, False)

  def step_2(self):
      GPIO.output(self.IN4, True)
      GPIO.output(self.IN3, True)
      sleep (self.time)
      GPIO.output(self.IN4, False)
      GPIO.output(self.IN3, False)

  def step_3(self):
      GPIO.output(self.IN3, True)
      sleep (self.time)
      GPIO.output(self.IN3, False)

  def step_4(self):
      GPIO.output(self.IN2, True)
      GPIO.output(self.IN3, True)
      sleep (self.time)
      GPIO.output(self.IN2, False)
      GPIO.output(self.IN3, False)

  def step_5(self):
      GPIO.output(self.IN2, True)
      sleep (self.time)
      GPIO.output(self.IN2, False)

  def step_6(self):
      GPIO.output(self.IN1, True)
      GPIO.output(self.IN2, True)
      sleep (self.time)
      GPIO.output(self.IN1, False)
      GPIO.output(self.IN2, False)

  def step_7(self):
      GPIO.output(self.IN1, True)
      sleep (self.time)
      GPIO.output(self.IN1, False)

  def step_8(self):
      GPIO.output(self.IN4, True)
      GPIO.output(self.IN1, True)
      sleep (self.time)
      GPIO.output(self.IN4, False)
      GPIO.output(self.IN1, False)

  def stepper_clockwise(self, steps):
    for i in range(steps):
      self.update_cur_pos(i)

      print(i)
      step_8() # could put these in an array, call them that way, reverse
      step_7()
      step_6()
      step_5()
      step_4()
      step_3()
      step_2()
      step_1()

  def stepper_counter_clockwise(self, steps):
    for i in range(steps):
      self.update_cur_pos(i)

      print(i)
      step_8() # could put these in an array, call them that way, reverse
      step_7()
      step_6()
      step_5()
      step_4()
      step_3()
      step_2()
      step_1()
  
  # the steppers face each other/rotations are flipped
  def zoom_in(self, steps):
    self.stepper_counter_clockwise(steps)

  def zoom_out(self, steps):
    self.stepper_clockwise(steps)

  def focus_close(self, steps):
    self.stepper_clockwise(steps)

  def focus_far(self, steps):
    self.stepper_counter_clockwise(steps)
