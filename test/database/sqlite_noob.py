import time
import sqlite3

con = sqlite3.connect("ml_hat_cam.db")
cur = con.cursor()

try:
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

def drop_db():
  cur.execute("DROP TABLE stepper_pos")

def update_pos(name, pos):
  cur.execute("UPDATE stepper_pos SET name = ?, pos = ? WHERE name = ?", [name, pos, name])
  con.commit()
  print('updated ' + str(time.time()))

# drop_db()
# init_db('tele')

# speed test
for step in range (0, 300, 1):
  update_pos('tele', step)
  time.sleep(0.01)
