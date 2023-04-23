# https://www.geeksforgeeks.org/python-program-find-ip-address
# https://stackoverflow.com/a/57355707/2710227
import socket

class Utils:
  def __init__(self):
    self.ip = '000.000.000.000'

  def get_ip(self):
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname + ".local")