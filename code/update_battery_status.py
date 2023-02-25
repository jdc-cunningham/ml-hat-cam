# this is ran by CRON every 5 minutes to increment the battery uptime
# it counts towards the max_uptime which means 100% usage is 0 capacity, recharge
# shouldn't let it get that high that's absolutely exhausted where battery protection
# kicks in for my particular batteries

import sys

sys.path.append('/home/pi/ml-hat-cam/code') # need this to resolve deps

from batt_db.batt_db import BattDatabase

batt_db = BattDatabase()
batt_db.update_batt_uptime()
