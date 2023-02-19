from database.database import Database
from lens_stepper.stepper import Stepper

db = Database()

focus_ring = Stepper(6, 13, 19, 26, 'focus', 350, db)
tele_ring = Stepper(12, 16, 20, 21, 'tele', 300, db)

def set_manual_values(pos):
  focus_ring.cur_pos = pos
  tele_ring.cur_pos = pos

  focus_ring.update_stepper_db_pos(pos)
  tele_ring.update_stepper_db_pos(pos)

def test_focus():
  print("init focus pos")
  print(focus_ring.get_pos())
  print("")

  focus_ring.focus_far(50)

  print(focus_ring.get_pos())
  print("")

  focus_ring.focus_near(50)

  print("at 0 " + str(focus_ring.get_pos()))
  print("")

  # at 0 here should not be able to go beyond

  # go beyond
  focus_ring.focus_near(50)

  print(focus_ring.get_pos())


def test_zoom():
  print("init zoom pos")
  print(tele_ring.get_pos())
  print("")

  tele_ring.zoom_in(50)

  print(tele_ring.get_pos())
  print("")

  tele_ring.zoom_out(50)

  print("at 0 " + str(tele_ring.get_pos()))
  print("")

  # at 0 here should not be able to go beyond

  # go beyond
  tele_ring.zoom_out(50)

  print(tele_ring.get_pos())

set_manual_values(0)
test_focus()
test_zoom()