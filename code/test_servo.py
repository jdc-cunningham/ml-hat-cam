# https://www.teachmemicro.com/raspberry-pi-pwm-servo-tutorial/

import pigpio
import time

pi = pigpio.pi()
focus_servo = 12
focus_pos = 500

tele_servo = 13
tele_pos = 500

def min_max():
  pi.set_servo_pulsewidth(focus_servo, 2500)
  time.sleep(5)

  for pw in range(2500,500,-1):
    pi.set_servo_pulsewidth(focus_servo, pw)
    time.sleep(0.001)

min_max()
