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
  dmenu.draw_text(0, 68, 'Yes')
  dmenu.draw_text(68, 68, 'No', '', 'CYAN')

def highlight_yes():
  dmenu.draw_text(68, 68, 'No', '', 'WHITE')
  dmenu.draw_text(0, 68, 'Yes', '', 'CYAN')

# def highlight_no():
#   #

draw_splash_screen()
time.sleep(3)
draw_charged_menu()
time.sleep(1)
highlight_yes()

control = Dpad(dmenu)
control.start()
