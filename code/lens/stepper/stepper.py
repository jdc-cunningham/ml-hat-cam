# based on
# https://github.com/custom-build-robots/Stepper-motor-28BYJ-48-Raspberry-Pi/blob/master/decision-maker.py

from time import sleep
import RPi.GPIO as GPIO

class Stepper:
  def __init__(self, pin1, pin2, pin3, pin4, name, max_pos):
    self.IN1 = pin1
    self.IN2 = pin2
    self.IN3 = pin3
    self.IN4 = pin4

    self.step_wait_time = 0.001
    self.name = name
    self.min_pos = 0 # assumes calibrated at max stop one side
    self.max_pos = max
    self.cur_pos = 0
    self.stop_moving = False

    self.init_gpio_pins()

  # this is a manual process, you need to catch the max pos by typing on keyboard/ssh
  # this should not have to be ran often
  # this is because the current physical design has no physical feedback on rotation position
  # other than focus of image
  def zero_stepper(self):
    self.step_wait_time = 0.01 # really slow it down for safety

    try:
      while True:
        if (self.name == 'tele'):
          self.zoom_out(1)
        else:
          self.focus_far(1)
    except KeyboardInterrupt:
      # back up, this is a source of error
      if (self.name == 'tele'):
        self.zoom_in(5)
      else:
        self.focus_near(5)
      self.stop_moving = True

  def update_cur_pos(self, step):
    if self.cur_pos < step:
      self.cur_pos = self.cur_pos - 1
    else:
      self.cur_pos = self.cur_pos + 1

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

  def step_1(self):
      GPIO.output(self.IN4, True)
      sleep (self.step_wait_time)
      GPIO.output(self.IN4, False)

  def step_2(self):
      GPIO.output(self.IN4, True)
      GPIO.output(self.IN3, True)
      sleep (self.step_wait_time)
      GPIO.output(self.IN4, False)
      GPIO.output(self.IN3, False)

  def step_3(self):
      GPIO.output(self.IN3, True)
      sleep (self.step_wait_time)
      GPIO.output(self.IN3, False)

  def step_4(self):
      GPIO.output(self.IN2, True)
      GPIO.output(self.IN3, True)
      sleep (self.step_wait_time)
      GPIO.output(self.IN2, False)
      GPIO.output(self.IN3, False)

  def step_5(self):
      GPIO.output(self.IN2, True)
      sleep (self.step_wait_time)
      GPIO.output(self.IN2, False)

  def step_6(self):
      GPIO.output(self.IN1, True)
      GPIO.output(self.IN2, True)
      sleep (self.step_wait_time)
      GPIO.output(self.IN1, False)
      GPIO.output(self.IN2, False)

  def step_7(self):
      GPIO.output(self.IN1, True)
      sleep (self.step_wait_time)
      GPIO.output(self.IN1, False)

  def step_8(self):
      GPIO.output(self.IN4, True)
      GPIO.output(self.IN1, True)
      sleep (self.step_wait_time)
      GPIO.output(self.IN4, False)
      GPIO.output(self.IN1, False)

  def stepper_clockwise(self, steps):
    for i in range(steps):
      if (self.stop_moving == True):
        return

      self.update_cur_pos(i)

      print(i)
      self.step_8() # could put these in an array, call them that way, reverse
      self.step_7()
      self.step_6()
      self.step_5()
      self.step_4()
      self.step_3()
      self.step_2()
      self.step_1()

  def stepper_counter_clockwise(self, steps):
    for i in range(steps):
      if (self.stop_moving == True):
        return

      self.update_cur_pos(i)

      print(i)
      self.step_8() # could put these in an array, call them that way, reverse
      self.step_7()
      self.step_6()
      self.step_5()
      self.step_4()
      self.step_3()
      self.step_2()
      self.step_1()
  
  # the steppers face each other/rotations are flipped
  def zoom_in(self, steps):
    self.stepper_counter_clockwise(steps)

  def zoom_out(self, steps):
    self.stepper_clockwise(steps)

  def focus_near(self, steps):
    self.stepper_clockwise(steps)

  def focus_far(self, steps):
    self.stepper_counter_clockwise(steps)
