import sqlite3
import traceback

class Database:
  def __init__(self):
    self.con = sqlite3.connect("ml_hat_cam_stepper.db", check_same_thread=False)
    self.init_stepper_pos_table()
    self.init_stepper_pos('tele')
    self.init_stepper_pos('focus')

  def get_con(self):
    return self.con

  def get_cursor(self):
    return self.con.cursor()

  def get_pos(self, cur, name):
    stepper_pos = cur.execute("SELECT pos FROM stepper_pos WHERE name = ?", [name])
    return stepper_pos.fetchone()[0]

  def init_stepper_pos_table(self):
    cur = self.get_cursor()
    table_exists = False

    try:
      table_exists = cur.execute("SELECT * FROM stepper_pos")
    except Exception:
      traceback.print_exc()
      table_exists = False

    if (not(table_exists)):
      try:
        cur.execute("CREATE TABLE stepper_pos(name, pos)")
      except Exception:
        print("create table error")
        traceback.print_exc()
  
  def init_stepper_pos(self, name):
    con = self.get_con()
    cur = self.get_cursor()
    stepper_pos = cur.execute("SELECT pos FROM stepper_pos WHERE name = ?", [name])
    res = stepper_pos.fetchone()

    if (res is None):
      cur.execute("INSERT INTO stepper_pos VALUES(?, ?)", [name, 0])
      con.commit()
    else:
      print("table entry exists")

  def drop_db(self):
    self.get_cursor().execute("DROP TABLE stepper_pos")

  def update_pos(self, name, pos, con, cur):
    cur.execute("UPDATE stepper_pos SET name = ?, pos = ? WHERE name = ?", [name, pos, name])
    con.commit()
    # print('updated ' + name + ' pos ' + str(pos) + ' ' + str(time.time()))

  def get_stepper_pos(self, cur, name):
    stepper_pos = cur.execute("SELECT pos FROM stepper_pos WHERE name = ?", [name])
    res = stepper_pos.fetchone()

    if (res is None):
      return 0
    
    return res[0]
