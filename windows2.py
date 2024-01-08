import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 불러오기
img = cv2.imread('C:/Users/user/Desktop/good.png', cv2.IMREAD_GRAYSCALE)

# 이미지 형태
print('img.shape: ', img.shape)

# 그림 크기 설정 (15, 15)는 너무 큼
plt.figure(figsize=(10, 10))

# 1. 이미지 이진화
_, binary_img = cv2.threshold(img, 29, 255, cv2.THRESH_BINARY)      # 29나 30이 적당
binary_img = binary_img // 255  # 0이랑 1로 정규화

# 2. y축 방향으로 픽셀 개수 세기
width = binary_img.shape[1]
step_size = 1
column_counts = []

for x in range(0, width, step_size):
    roi = binary_img[:, x:x+step_size]
    count = np.sum(roi)
    column_counts.append(count)

# 3. 그래프 생성
x_coords = list(range(0, width, step_size))
plt.subplot(2, 2, 2)  # 1사분면에 그래프 표시
plt.plot(x_coords, column_counts)
plt.xlabel('x axis pixel')  # x축 이름
plt.ylabel('num of pixel is 1')  # y축 이름
plt.title('Pixel Distribution')  # 그래프 제목

# 4. 평균과 표준편차 계산 및 출력
mean_count = np.mean(column_counts)
std_dev = np.std(column_counts)

# 배율 값 입력 및 적용
scale_factor = float(input("배율값 입력: ") or 1.0)
mean_count *= scale_factor
std_dev *= scale_factor

# 5. 4분할 화면에 표시
plt.subplot(2, 2, 1)  # 2사분면에 원본 이미지 표시
plt.imshow(img, cmap='gray')
plt.title('Original Image')

plt.subplot(2, 2, 3)  # 3사분면에 이진화 이미지 표시
plt.imshow(binary_img, cmap='gray')
plt.title('Binary Image')

plt.subplot(2, 2, 4)  # 4사분면에 평균, 표준편차 표시
plt.text(0.1, 0.6, f'Mean: {mean_count:.2f}', fontsize=12)
plt.text(0.1, 0.4, f'Standard Deviation: {std_dev:.2f}', fontsize=12)
plt.text(0.1, 0.2, f'Scale Factor: {scale_factor}', fontsize=12)
plt.axis('off')  # 4사분면 테두리 제거

plt.tight_layout()
plt.subplots_adjust(hspace=0.5)  # 세로 간격 조절
plt.show()
