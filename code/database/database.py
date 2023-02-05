import time
import sqlite3
import traceback

from threading import Thread

class Database:
  def __init__(self):
    self.con = sqlite3.connect("ml_hat_cam.db", check_same_thread=False)
    self.init_stepper_pos_table()
    self.init_stepper_pos('zoom')
    self.init_stepper_pos('focus')

  def get_con(self):
    return self.con

  def get_cursor(self):
    return self.con.cursor()

  def get_pos(self, cur, name):
    return cur.execute("SELECT pos FROM stepper_pos WHERE name = ?", [name])

  def init_stepper_pos_table(self):
    try:
      cur = self.get_cursor()
      cur.execute("CREATE TABLE stepper_pos(name, pos)")
    except Exception:
      print("create table error")
      traceback.print_exc()
  
  def init_stepper_pos(self, name):
    con = self.get_con()
    cur = self.get_cursor()
    stepper_pos = cur.execute("SELECT pos FROM stepper_pos WHERE name = ?", [name])
    res = stepper_pos.fetchall()

    if (len(res) == 0):
      cur.execute("INSERT INTO stepper_pos VALUES(?, ?)", [name, 0])
      con.commit()
    else:
      print(len(res))

  def drop_db(self):
    self.get_cursor().execute("DROP TABLE stepper_pos")

  def update_pos(self, name, pos, con, cur):
    cur.execute("UPDATE stepper_pos SET name = ?, pos = ? WHERE name = ?", [name, pos, name])
    con.commit()
    print('updated ' + name + ' pos ' + str(pos) + ' ' + str(time.time()))

  def get_stepper_pos(self, cur, name):
    stepper_pos = cur.execute("SELECT pos FROM stepper_pos WHERE name = ?", [name])
    res = stepper_pos.fetchall()

    if (len(res) == 0):
      return 0
    
    return res[0]
