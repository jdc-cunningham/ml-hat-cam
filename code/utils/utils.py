# https://www.geeksforgeeks.org/python-program-find-ip-address
import socket

class Utils:
  def __init__(self):
    self.ip = '000.000.000.000'

  def get_ip(self):
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)