# references
# https://github.com/custom-build-robots/Stepper-motor-28BYJ-48-Raspberry-Pi/blob/master/decision-maker.py
# https://raspberrypi.stackexchange.com/questions/5100/detect-that-a-python-program-is-running-on-the-pi
import os

from time import sleep

on_pi = not(os.name == 'nt') # assumes only two OS environments

if on_pi: import RPi.GPIO as GPIO

# from stepper_steps import stepper_clockwise, stepper_counter_clockwise

class Stepper:
  from .stepper_steps import stepper_clockwise, stepper_counter_clockwise

  def __init__(self, pin1, pin2, pin3, pin4, name, max_pos, db):
    self.on_pi = on_pi
    self.IN1 = pin1
    self.IN2 = pin2
    self.IN3 = pin3
    self.IN4 = pin4

    self.step_wait_time = 0.001
    self.name = name
    self.min_pos = 0 # assumes calibrated at max stop one side
    self.max_pos = max_pos
    self.stop_moving = False
    self.db = db
    self.db_con = db.get_con()
    self.db_cur = db.get_cursor()
    self.cur_pos = db.get_stepper_pos(self.db_cur, self.name)
    self.db_update_pos = db.update_pos
    self.ignore_db = False
    self.GPIO = GPIO
    self.sleep = sleep

    if on_pi:
      self.init_gpio_pins()
      self.zero_stepper()

  def zero_stepper(self):
    prev_pos = self.get_pos()

    if self.name == 'focus':
      self.focus_near(prev_pos)
    else:
      self.zoom_out(prev_pos)

  def init_gpio_pins(self):
    GPIO.setwarnings(False) # this is not great, but this class instance is not intended to be destroyed
    GPIO.setmode(GPIO.BCM)

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

  def get_pos(self):
    return self.db.get_pos(self.db_cur, self.name)

  def get_current_focal_length(self):
    step_per_mm = 7.14 # (50-8/300)
    return self.cur_pos * step_per_mm

  # this is a manual process, you need to catch the max pos by typing on keyboard/ssh
  # this should not have to be ran often
  # this is because the current physical design has no physical feedback on rotation position
  # other than focus of image
  def zero_stepper_manual(self):
    self.step_wait_time = 0.01 # really slow it down for safety
    self.ignore_db = True

    try:
      while True:
        if (self.name == 'tele'):
          self.zoom_out(1)
        else:
          self.focus_near(1)
    except KeyboardInterrupt:
      # back up, this is a source of error
      if (self.name == 'tele'):
        self.zoom_in(15)
      else:
        self.focus_far(15)
      self.update_stepper_db_pos(0)
      self.stop_moving = True
      self.ignore_db = False

  def update_cur_pos(self, steps, step_op):
    if (step_op == 'subtract' and (self.cur_pos - steps) < 0):
      return False

    if (step_op == 'add' and (steps + self.cur_pos) > self.max_pos):
      return False

    if step_op == 'add':
      self.cur_pos = self.cur_pos + steps
    else:
      self.cur_pos = self.cur_pos - steps

    return True

  def update_stepper_db_pos(self, step):
    self.db_update_pos(self.name, step, self.db_con, self.db_cur)

  # the steppers face each other/rotations are flipped
  # self.on_pi check skips calling steppers if no on pi
  def zoom_in(self, steps):
    if (self.name == 'focus'): return False
    if (not self.update_cur_pos(steps, 'add')): return False
    moved = True if not self.on_pi else self.stepper_clockwise(steps)
    if self.ignore_db: return False
    if moved: self.update_stepper_db_pos(self.cur_pos)

  def zoom_out(self, steps):
    if (self.name == 'focus'): return False
    if (not self.update_cur_pos(steps, 'subtract')): return False
    moved = True if not self.on_pi else self.stepper_counter_clockwise(steps)
    if self.ignore_db: return False
    if moved: self.update_stepper_db_pos(self.cur_pos)

  def focus_near(self, steps):
    if (self.name == 'tele'): return False
    if (not self.update_cur_pos(steps, 'subtract')): return False
    moved = True if not self.on_pi else self.stepper_counter_clockwise(steps)
    if self.ignore_db: return False
    if moved: self.update_stepper_db_pos(self.cur_pos)

  def focus_far(self, steps):
    if (self.name == 'tele'): return False
    if (not self.update_cur_pos(steps, 'add')): return False
    moved = True if not self.on_pi else self.stepper_clockwise(steps)
    if self.ignore_db: return False
    if moved: self.update_stepper_db_pos(self.cur_pos)
