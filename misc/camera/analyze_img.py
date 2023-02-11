import time
import numpy as np
import cv2 as cv

from matplotlib import pyplot as plt

img = cv.imread('test.jpeg',0)

print(time.time())
edges = cv.Canny(img,100,200)
print(time.time())

print(len(edges))
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()
