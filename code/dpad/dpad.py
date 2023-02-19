# https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/

import RPi.GPIO as GPIO
import time

class Dpad:
  def __init__(self, dmenu):
    self.display = dmenu

    # GPIO should be set by steppers already
    GPIO.setmode(GPIO.BCM) # match stepper mode
    GPIO.setup(0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # UP
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # RIGHT
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # CENTER
    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # LEFT
    GPIO.setup(1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # DOWN

  # listen for input
  def start(self):
    while True:
      if GPIO.input(24) == GPIO.HIGH:
        print("RIGHT")
        self.display.draw_text(0, 0, "RIGHT")
      if GPIO.input(0) == GPIO.HIGH:
        print("UP")
        self.display.draw_text(0, 0, "UP")
      if GPIO.input(5) == GPIO.HIGH:
        print("CENTER")
        self.display.draw_text(0, 0, "CENTER")
      if GPIO.input(7) == GPIO.HIGH:
        print("LEFT")
        self.display.draw_text(0, 0, "LEFT")
      if GPIO.input(1) == GPIO.HIGH:
        print("DOWN")
        self.display.draw_text(0, 0, "DOWN")

      time.sleep(0.05)
