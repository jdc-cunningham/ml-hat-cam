import os
import sqlite3
import traceback

base_path = "/home/pi/ml-hat-cam/code" # due to CRON

class BattDatabase:
  def __init__(self):
    self.con = sqlite3.connect(base_path + "/ml_hat_cam_batt.db", check_same_thread=False)
    self.init_batt_table()

  def get_con(self):
    return self.con
  
  def get_cursor(self):
    return self.con.cursor()

  def init_batt_table(self):
    con = self.get_con()
    cur = self.get_cursor()
    table_exists = False

    try:
      table_exists = cur.execute("SELECT * FROM battery_status")
    except Exception:
      traceback.print_exc()
      table_exists = False

    if (not(table_exists)):
      try:
        # ids could be useful if switching batteries
        cur.execute("CREATE TABLE battery_status(uptime, max_uptime)") # minute units
        cur.execute("INSERT INTO battery_status VALUES(?, ?)", [0, 300]) # 345 is max depleted
        con.commit()
      except Exception:
        print("create table error")
        traceback.print_exc()

  def get_uptime_info(self):
    cur = self.get_cursor()
    # this is dumb, but having issues where id column even non-rowid can't be found by CRON update call
    uptime = cur.execute("SELECT uptime, max_uptime FROM battery_status LIMIT 1")
    res = uptime.fetchone()

    if (res is None):
      return [0, 300] # disconnect with seed
    
    return res

  def update_batt_uptime(self):
    con = self.get_con()
    cur = self.get_cursor()
    prev_uptime = self.get_uptime_info()
    res = prev_uptime
    
    if (res is None):
      res = 0

    new_val = res[0] + 5

    cur.execute("UPDATE battery_status SET uptime = ? WHERE rowid = 1", [new_val])
    con.commit()

  def reset_uptime(self):
    con = self.get_con()
    cur = self.get_cursor()
    cur.execute("UPDATE battery_status SET uptime = ? WHERE rowid = 1", [0])
    con.commit()

  def get_batt_status(self):
    uptime = self.get_uptime_info()

    if (uptime is None):
      return "100%"
    
    used_per = (uptime[0] / uptime[1]) * 100
    left_over = round(100 - used_per, 2)

    return str(left_over) + "%"