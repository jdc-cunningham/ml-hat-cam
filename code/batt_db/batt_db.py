import sqlite3
import traceback

class BattDatabase:
  def __init__(self):
    self.con = sqlite3.connect("ml_hat_cam_batt.db", check_same_thread=False)
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
        cur.execute("CREATE TABLE battery_status(uptime, max_uptime)") # minute units
        cur.execute("INSERT INTO battery_status VALUES(?, ?)", [0, 345])
        con.commit()
      except Exception:
        print("create table error")
        traceback.print_exc()

  def update_batt_uptime(self, uptime):
    con = self.get_con()
    cur = self.get_cursor()
    prev_uptime = cur.execute("SELECT uptime FROM battery_pos LIMIT 1")
    res = prev_uptime.fetchone()
    
    if (res is None):
      res = 0

    new_val = res + uptime

    cur.execute("UPDATE battery_status SET uptime = ?, pos = ? WHERE name = ?", [new_val])
    con.commit()

  def reset_uptime(self):
    con = self.get_con()
    cur = self.get_cursor()
    cur.execute("UPDATE battery_status SET uptime = ?, pos = ? WHERE name = ?", [0])
    con.commit()

  def get_batt_status(self):
    cur = self.get_cursor()
    uptime = cur.execute("SELECT uptime, max_uptime FROM battery_status LIMIT 1")
    res = uptime.fetchone()

    if (res is None):
      return "100%"
    
    return str(round(100 - ((res[0] / res[1]) * 100, 2))) + "%"