#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

# resources
# https://www.geeksforgeeks.org/python-pil-image-frombuffer-method/
# https://stackoverflow.com/questions/22879991/buffer-to-image-with-pil

import io
import logging
import socketserver
import time
import cv2 as cv
import numpy as np

from io import BytesIO
from http import server
from threading import Condition, Thread
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from PIL import Image

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


# https://stackoverflow.com/a/55360543/2710227
def get_img_edge_count(frame_buffer):
    img = cv.imdecode(frame_buffer, cv.IMREAD_COLOR)
    edges = cv.Canny(img,100,200)
    sum_edges = 0

    for i in range (0, len(edges), 1):
        sum_edges += np.count_nonzero(edges[0])

    return sum_edges

prev_edge_count = 0

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        stream_count = 0

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

                    # print('')
                    stream_count += 1
                    # print(time.time())

                    if (stream_count % 2 == 0):
                        sample_img = np.fromstring(frame, np.uint8)
                        edges = get_img_edge_count(sample_img)

                        print(edges)

                    # if (edges > 0 and edges > prev_edge_count):
                    #     print("better")
                    # else:
                    #     print("worse")

                    # print()
                    # print(time.time())
                    print('')

                    # sample_img = Image.open(BytesIO(frame))
                    # sample_img.save("test.jpeg", "JPEG")
                    # print(time.time())
                    # return

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


picam2 = Picamera2()
# picam2.configure(picam2.create_video_configuration(main={"size": (1024, 720)}))
picam2.configure(picam2.create_video_configuration(main={"size": (600, 400)}))
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    picam2.stop_recording()
