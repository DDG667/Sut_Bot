import cv2
import numpy as np

img = np.ones([8192, 4096, 3], dtype=np.int8) * 16
cv2.imwrite("bg.jpg", img)
