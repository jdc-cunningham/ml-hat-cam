import time
import sqlite3
import threading
from threading import Thread

con = sqlite3.connect("ml_hat_cam.db", check_same_thread=False)

try:
  cur = con.cursor()
  cur.execute("CREATE TABLE stepper_pos(name, pos)")
except:
  print("db exists or error")

def init_db(name):
  stepper_pos = cur.execute("SELECT pos FROM stepper_pos WHERE name = ?", [name])
  res = stepper_pos.fetchall()

  if (len(res) == 0):
    cur.execute("INSERT INTO stepper_pos VALUES(?, ?)", [name, 0])
    con.commit()
  else:
    print(len(res))

def drop_db(cur):
  cur.execute("DROP TABLE stepper_pos")

def update_pos(name, pos, cur):
  cur.execute("UPDATE stepper_pos SET name = ?, pos = ? WHERE name = ?", [name, pos, name])
  con.commit()
  print('updated ' + name + ' pos ' + str(pos) + ' ' + str(time.time()))

# cur = con.cursor()
# drop_db(cur)
init_db('zoom')
init_db('focus')

# threading test
def focus_stepper():
  cur = con.cursor()
  time.sleep(1)

  for step in range (0, 300, 1):
    update_pos('zoom', step, cur)
    time.sleep(0.01)

def tele_stepper():
  cur = con.cursor()
  time.sleep(1)

  for step in range (0, 300, 1):
    update_pos('focus', step, cur)
    time.sleep(0.01)

Thread(target=focus_stepper).start()
Thread(target=tele_stepper).start()