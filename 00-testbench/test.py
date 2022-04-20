import os
import numpy as np
import cv2

file = 'datasets\\surfer\\0001.jpg'
img = cv2.imread(file, 0)
img_flatten = img.flatten()
print('img_flatten:', img_flatten.shape)
img_ = np.concatenate([img_flatten[100:], img_flatten[0:100]])
img_ = img_.reshape(img.shape)
cv2.imshow('orginal', img)
cv2.imshow('shift', img_)
cv2.waitKey(0)
cv2.destroyAllWindows()
