import subprocess

class UsbStorage():
  def __init__(self):
    self.mounted = False

  def check_mounted(self):
     # sdb1 confirmed beforehand with lsblk
    self.mounted = subprocess.check_output('mount /dev/sdb1 /mnt', shell=True) == 0
