from sshkeyboard import listen_keyboard

from stepper.stepper import Stepper

step_incr = 10

def stepper_controls(key):
  if (key == 'up'): # zoom_in

  if (key == 'down'): # zoom_out
    

def press(key):
  print(f"'{key}' pressed")

def release(key):
  print(f"'{key}' released")

listen_keyboard(
  on_press=press,
  on_release=release,
  # delay_second_char=0.75,
  # delay_other_chars=0.05
)
