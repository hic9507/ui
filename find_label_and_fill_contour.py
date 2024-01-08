import os
import cv2
import numpy as np

img = cv2.imread('C:/Users/user/Desktop/windows/20230111_162711.png', cv2.IMREAD_GRAYSCALE)

# 1. 이미지 이진화
_, binary_img = cv2.threshold(img, 29, 255, cv2.THRESH_BINARY)
binary_img = binary_img // 255  # Convert pixel values to 0 or 1
adap_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)

# 라벨링
num_labels, labels = cv2.connectedComponents(binary_img)
adap_num_labels, adap_labels = cv2.connectedComponents(adap_img)

# 각 라벨에 대한 픽셀 수 계산
area_count = np.bincount(labels.ravel())
adap_area_count = np.bincount(adap_labels.ravel())

# 0은 배경이므로 무시
area_count[0] = 0
adap_area_count[0] = 0

# 가장 큰 라벨 찾기
largest_label = area_count.argmax()
adap_largest_label = adap_area_count.argmax()

# 결과 이미지 생성
largest_component = (labels == largest_label).astype(np.uint8)
adap_largest_component = (adap_labels == adap_largest_label).astype(np.uint8)

# 외곽선(contour) 찾기
contours, _ = cv2.findContours(largest_component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
adap_contours, adap__ = cv2.findContours(adap_largest_component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 외곽선으로 영역 채워 넣기
cv2.drawContours(largest_component, contours, -1, (1), thickness=cv2.FILLED)
cv2.drawContours(adap_largest_component, adap_contours, -1, (1), thickness=cv2.FILLED)

result_img = largest_component * 255  # Convert back to 0-255 scale
result_img = cv2.resize(result_img, (512, 512))
adap_result_img = adap_largest_component * 255
adap_result_img = cv2.resize(adap_result_img, (512, 512))

final_img = np.hstack((result_img, cv2.resize(img, (512, 512))))
adap_final_img = np.hstack((adap_result_img, cv2.resize(img, (512, 512))))

# 이미지 표시
cv2.imshow('Result Image', result_img)
cv2.imshow('final_img', final_img)
cv2.imshow('adap_result_img', adap_final_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
