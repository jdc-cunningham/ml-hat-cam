import os, sys, time

lib_dir = os.getcwd() + '/display_menu'
sys.path.append(lib_dir)

from display_menu.display_menu import DisplayMenu
from dpad.dpad import Dpad  

dmenu = DisplayMenu()

def draw_splash_screen():
  dmenu.draw_text(0, 55, 'ML Hat Cam v1')

def draw_charged_menu():
  dmenu.clear()
  dmenu.draw_text(0, 46, 'Charged?')
  dmenu.draw_text(0, 68, '  Yes         No')
  dmenu.draw_line([64, 68], [64, 88])   # left
  dmenu.draw_line([64, 88], [127, 88])  # bottom
  dmenu.draw_line([127, 68], [127, 88]) # right
  dmenu.draw_line([64, 68], [127, 68])  # top

def draw_left_box():
  # hide existing white box
  dmenu.draw_line([64, 68], [64, 88], "BLACK")
  dmenu.draw_line([64, 88], [127, 88], "BLACK")
  dmenu.draw_line([127, 68], [127, 88], "BLACK")
  dmenu.draw_line([64, 68], [127, 68], "BLACK")

  dmenu.draw_line([0, 68], [0, 88])
  dmenu.draw_line([0, 88], [64, 88])
  dmenu.draw_line([64, 68], [64, 88])
  dmenu.draw_line([0, 68], [64, 68])

draw_splash_screen()
time.sleep(3)
draw_charged_menu()
time.sleep(1)
draw_left_box()

control = Dpad(dmenu)
control.start()
