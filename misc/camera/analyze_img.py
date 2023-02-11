import time
import numpy as np
import cv2 as cv
import json
import numpy
from statistics import mean

from matplotlib import pyplot as plt

img = cv.imread('in-focus.JPG',0)

def canny_edge(img):
  print(time.time())
  edges = cv.Canny(img,100,200)
  print(time.time())

  sum_edges = 0

  for i in range (0, len(edges), 1):
    sum_edges += numpy.count_nonzero(edges[0])

  print(sum_edges)

# https://stackoverflow.com/questions/48319918/whats-the-theory-behind-computing-variance-of-an-image
def variance(img):
  return cv.Laplacian(img, cv.CV_64F).var()

# **2 is power of 2/squared
def variance_x(var_arr):
  print(var_arr)
  return mean(abs(var_arr - var_arr.mean())**2)

var_arr = variance(img)
print(var_arr)
# print(variance_x(var_arr))

# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()
