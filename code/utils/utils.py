import os

class Utils:
  def __init__(self):
    self.ip = '000.000.000.000'

  # https://stackoverflow.com/a/3503909/2710227
  def get_ip(self):
    ifconfig_out = os.popen('ifconifg').read()
    local_ip = '192' + ifconfig_out.split('inet 192')[1].split('  netmask')[0]

    return local_ip or 'no ip' # can happen not on wifi