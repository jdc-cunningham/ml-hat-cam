import io
import logging
import socketserver
import cv2 as cv
import numpy as np

from http import server
from threading import Condition, Thread

PAGE = """\
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
  def __init__(self):
    self.frame = None
    self.condition = Condition()

  def write(self, buf):
    with self.condition:
      self.frame = buf
      self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
  def __init__(self, focus_ring, tele_ring):
    self.focus_ring = focus_ring
    self.tele_ring = tele_ring
    self.stream_count = 0

  def get_variance(frame_buffer):
    img = cv.imdecode(frame_buffer, cv.IMREAD_COLOR)
    return cv.Laplacian(img, cv.CV_64F).var()

  def do_GET(self):
    if self.path == '/':
      self.send_response(301)
      self.send_header('Location', '/index.html')
      self.end_headers()
    elif self.path == '/index.html':
      content = PAGE.encode('utf-8')
      self.send_response(200)
      self.send_header('Content-Type', 'text/html')
      self.send_header('Content-Length', len(content))
      self.end_headers()
      self.wfile.write(content)
    elif self.path == '/stream.mjpg':
      self.send_response(200)
      self.send_header('Age', 0)
      self.send_header('Cache-Control', 'no-cache, private')
      self.send_header('Pragma', 'no-cache')
      self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
      self.end_headers()

      try:
        while True:
          with output.condition:
            output.condition.wait()
            frame = output.frame

          self.wfile.write(b'--FRAME\r\n')
          self.send_header('Content-Type', 'image/jpeg')
          self.send_header('Content-Length', len(frame))
          self.end_headers()
          self.wfile.write(frame)
          self.wfile.write(b'\r\n')

          self.stream_count += 1

          if (self.stream_count % 2 == 0):
            sample_img = np.fromstring(frame, np.uint8)
            print(self.get_variance(frame))

      except Exception as e:
        logging.warning(
          'Removed streaming client %s: %s',
          self.client_address, str(e))
    else:
      self.send_error(404)
      self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
  allow_reuse_address = True
  daemon_threads = True
