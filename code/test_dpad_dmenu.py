import os, sys

lib_dir = os.getcwd() + '/display_menu'
sys.path.append(lib_dir)

from display_menu.display_menu import DisplayMenu
from dpad.dpad import Dpad

dmenu = DisplayMenu()
dmenu.draw_text(0, 0, 'huh')
control = Dpad()
control.start(dmenu)
