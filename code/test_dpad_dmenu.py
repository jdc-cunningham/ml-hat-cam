import os, sys

lib_dir = os.getcwd() + '/display_menu'
sys.path.append(lib_dir)

from display_menu.display_menu import DisplayMenu
from dpad.dpad import Dpad

dmenu = DisplayMenu()
control = Dpad(dmenu)
control.start()
