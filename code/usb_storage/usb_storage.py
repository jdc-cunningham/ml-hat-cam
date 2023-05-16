import subprocess

class UsbStorage():
  def __init__(self):
    self.mounted = False

  def check_mounted(self):
     # sdb1 confirmed beforehand with lsblk
    trya = subprocess.check_output('mount /dev/sda1 /mnt', shell=True) == 0

    if (trya != 0):
      tryb = subprocess.check_output('mount /dev/sda1 /mnt', shell=True) == 0

    self.mounted = trya == 0 or tryb == 0 # what
