import sys, os
import cv2
import numpy as np
from matplotlib import pyplot as plt

# f = open('output.text', 'r')
# f.close()

# with open('output.text', 'r') as f:
#     ex = f.read()
#     for i in ex:
#         if i != 1 and i != 0:
#             print(i)

img = cv2.imread("C:/Users/user/Desktop/windows/20230111_162711.png", cv2.IMREAD_GRAYSCALE)

_, binary_img = cv2.threshold(img, 29, 255, cv2.THRESH_BINARY)
# binary_img = binary_img // 255
cv2.imshow('binary_img', cv2.resize(binary_img, (512, 512)))


num_labels, labels = cv2.connectedComponents(binary_img)

area_count = np.bincount(labels.ravel())
area_count[0] = 0
largest_label = area_count.argmax()
largest_component = (labels == largest_label).astype(np.uint8)

contours, _ = cv2.findContours(largest_component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
filled_img = cv2.drawContours(np.zeros_like(largest_component), contours, -1, (1), thickness=cv2.FILLED)

processed_img = filled_img * 255
processed_img = cv2.resize(processed_img, (512, 512))
print('image shape: ', processed_img.shape)

cv2.imshow('processed_img', processed_img)
cv2.waitKey()