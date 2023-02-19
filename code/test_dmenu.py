import os, sys

lib_dir = os.getcwd() + '/display_menu'
# pic_dir = os.getcwd() + '/display_menu/pic'

sys.path.append(lib_dir)
# sys.path.append(pic_dir)

from display_menu.display_menu import DisplayMenu

dmenu = DisplayMenu()

dmenu.draw_text(0, 0, 'huh')
