# https://www.geeksforgeeks.org/python-os-path-ismount-method/#
import os
import subprocess

class UsbStorage():
  def __init__(self):
    self.mounted = False
    self.mount_path = '/mnt'

  def check_mounted(self):
    if (os.path.ismount(self.mount_path)):
      return True # not necessarily the right device, but code below assigns it

     # sdb1 confirmed beforehand with lsblk
    trya = subprocess.check_output('mount /dev/sda1 /mnt', shell=True) == 0

    if (trya != 0):
      tryb = subprocess.check_output('mount /dev/sda1 /mnt', shell=True) == 0

    self.mounted = trya == 0 or tryb == 0 # what
    return self.mounted
