import time
import numpy as np
import cv2 as cv
import json
import numpy

from matplotlib import pyplot as plt

# img = cv.imread('blurry.JPG',0)
img = cv.imread('check.JPG',0)

print(time.time())
edges = cv.Canny(img,100,200)
print(time.time())

sum_edges = 0

for i in range (0, len(edges), 1):
  sum_edges += numpy.count_nonzero(edges[0])

print(sum_edges)

# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()
