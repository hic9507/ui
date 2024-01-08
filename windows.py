import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('C:/Users/user/Desktop/good.png', cv2.IMREAD_GRAYSCALE)

# 1. 이미지 이진화
_, binary_img = cv2.threshold(img, 29, 255, cv2.THRESH_BINARY)
binary_img = binary_img // 255  # Convert pixel values to 0 or 1

# 2. y축 방향으로 픽셀 개수 세기
width = binary_img.shape[1]
step_size = 2
column_counts = []

for x in range(0, width, step_size):
    roi = binary_img[:, x:x+step_size]
    count = np.sum(roi)
    column_counts.append(count)

# 3. 그래프 생성
x_coords = list(range(0, width, step_size))
plt.subplot(2, 2, 2)  # 1사분면에 꺾은선 그래프 표시
plt.plot(x_coords, column_counts)
plt.xlabel('Position along X-axis')  # x축 이름
plt.ylabel('Number of 1s along Y-axis')  # y축 이름
plt.title('Pixel Distribution')  # 그래프 제목

# 4. 평균과 표준편차 계산 및 출력
mean_count = np.mean(column_counts)
std_dev = np.std(column_counts)

# 배율 값 입력 및 적용
scale_factor = float(input("Enter the scale factor (default is 1.0): ") or 1.0)
mean_count *= scale_factor
std_dev *= scale_factor

# 5. 4분할 화면에 표시
plt.subplot(2, 2, 1)  # 2사분면에 원본 이미지 표시
plt.imshow(img, cmap='gray')
plt.title('Original Image')  # 원본 이미지 제목

plt.subplot(2, 2, 3)  # 3사분면에 이진화 이미지 표시
plt.imshow(binary_img, cmap='gray')
plt.title('Binary Image')  # 이진화 이미지 제목

plt.subplot(2, 2, 4)  # 4사분면에 평균, 표준편차 표시
plt.text(0.1, 0.6, f'Mean: {mean_count:.2f}', fontsize=12)
plt.text(0.1, 0.4, f'Std Dev: {std_dev:.2f}', fontsize=12)
plt.text(0.1, 0.2, f'Scale Factor: {scale_factor}', fontsize=12)
plt.axis('off')  # 축 정보를 숨김

plt.tight_layout()
plt.show()
