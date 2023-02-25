# this is ran by CRON every 5 minutes to increment the battery uptime
# it counts towards the max_uptime which means 100% usage is 0 capacity, recharge
# shouldn't let it get that high that's absolutely exhausted where battery protection
# kicks in for my particular batteries

import os, sys

lib_dir = os.getcwd() + '/display_menu'
sys.path.append(lib_dir)

from display_menu.display_menu import DisplayMenu
from batt_db.batt_db import BattDatabase

batt_db = BattDatabase()
batt_db.update_batt_uptime()
dmenu = DisplayMenu()

batt_status = batt_db.get_batt_status()
dmenu.draw_text(0, 0, 'batt: ' + batt_status, 'font_1', 'WHITE')

# hmm... need long-running service access even from cron/systemd
