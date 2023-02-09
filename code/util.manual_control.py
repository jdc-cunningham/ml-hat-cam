from sshkeyboard import listen_keyboard
from database.database import Database
from lens.stepper.stepper import Stepper

step_incr = 10

db = Database()

tele_ring = Stepper(12, 16, 20, 21, 'tele', 300, db)
focus_ring = Stepper(6, 13, 19, 26, 'focus', 350, db)

def stepper_controls(key):
  if (key == 'up' or key == 'down'):
    print("pos " + str(tele_ring.cur_pos))

  if (key == 'left' or key == 'right'):
    print("pos " + str(focus_ring.cur_pos))

  if (key == 'up'):
    tele_ring.zoom_in(step_incr)

  if (key == 'down'):
    tele_ring.zoom_out(step_incr)

  if (key == 'left'):
    focus_ring.focus_near(step_incr)

  if (key == 'right'):
    focus_ring.focus_far(step_incr)

def press(key):
  print(f"'{key}' pressed")
  stepper_controls(key)

def release(key):
  print(f"'{key}' released")

listen_keyboard(
  on_press=press,
  on_release=release,
  # delay_second_char=0.75,
  # delay_other_chars=0.05
)
