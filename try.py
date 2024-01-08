import os, cv2
import numpy as np



file_path = 'C:/Users/user/Desktop/windows/20230111_162711.png'

img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
_, binary_img = cv2.threshold(img, 29, 255, cv2.THRESH_BINARY)
binary_img = binary_img // 255

# Filling small holes 모폴로지 연산: filling 사용
kernel = np.ones((5, 5), np.uint8)
filled_binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

num_labels, labels = cv2.connectedComponents(filled_binary_img)

area_count = np.bincount(labels.ravel())
area_count[0] = 0
largest_label = area_count.argmax()
largest_component = (labels == largest_label).astype(np.uint8)

contours, _ = cv2.findContours(largest_component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# contour 스무딩
epsilon = 0.01 * cv2.arcLength(contours[0], True)
smoothed_contour = [cv2.approxPolyDP(contours[0], epsilon, True)]

filled_img = cv2.drawContours(np.zeros_like(largest_component), smoothed_contour, -1, (1), thickness=cv2.FILLED)

processed_img = filled_img * 255

##### adaptive threshold

img1 = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
mean_binary_img = cv2.adaptiveThreshold(img1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 1001, 10)
gaussian_binary_img = cv2.adaptiveThreshold(img1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 1001, 10)
cv2.imshow('mean_binary_img', cv2.resize(mean_binary_img, (400, 400)))
cv2.imshow('gaussian_binary_img', cv2.resize(gaussian_binary_img, (400, 400)))
cv2.imshow('original img', cv2.resize(img, (400, 400)))

print('image shape: ', processed_img.shape)
cv2.imshow('processed_img', cv2.resize(processed_img, (400, 400)))


a = np.hstack((cv2.resize(img, (400, 400)), cv2.resize(processed_img, (400, 400))))
b = np.hstack((cv2.resize(mean_binary_img, (400, 400)), cv2.resize(gaussian_binary_img, (400, 400))))
c = np.vstack((a, b))
cv2.imshow('c', c)
cv2.waitKey()
