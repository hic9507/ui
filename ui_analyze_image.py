import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def analyze_image(img_path, scale_factor=1.0):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    # 1. 이미지 이진화
    _, binary_img = cv2.threshold(img, 29, 255, cv2.THRESH_BINARY)      # 29나 30이 적당
    binary_img = binary_img // 255

    # 2. y축 방향으로 픽셀 개수 세기
    width = binary_img.shape[1]
    step_size = 1
    column_counts = [np.sum(binary_img[:, x:x + step_size]) for x in range(0, width, step_size)]

    # 그림 크기 설정 (15, 15)는 너무 큼
    fig = plt.figure(figsize=(20, 20))

    # 3. 그래프 생성
    plt.subplot(2, 2, 2)        # 1사분면 그래프
    plt.plot(column_counts)
    plt.xlabel('x axis pixel')
    plt.ylabel('num of pixel is 1')
    plt.title('Pixel Distribution')

    plt.subplot(2, 2, 1)        # 2사분면 원본 이미지
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')

    plt.subplot(2, 2, 3)        # 3사분면 이진화 이미지
    plt.imshow(binary_img, cmap='gray')
    plt.title('Binary Image')

    plt.subplot(2, 2, 4)        # 4사분면 평균값, 표준편차, 배율값 표시
    mean_count = np.mean(column_counts)
    std_dev = np.std(column_counts)
    mean_count *= scale_factor
    std_dev *= scale_factor
    plt.text(0.1, 0.6, f'Mean: {mean_count:.2f}', fontsize=25)
    plt.text(0.1, 0.4, f'Std Dev: {std_dev:.2f}', fontsize=25)
    plt.text(0.1, 0.2, f'Scale Factor: {scale_factor}', fontsize=25)
    plt.axis('off')

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.5, wspace=0.5)

    return fig

def on_analyze_button_click():
    scale_factor = float(scale_factor_entry.get())
    fig = analyze_image(img_path, scale_factor)
    if fig:
        for widget in frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()

        # UI 요소 다시 배치
        layout_ui_elements()

app = tk.Tk()
app.title("Image Analyzer")
app.geometry('1100x800')

# 색, 스타일 설정
app.configure(bg='#3498db')
style = ttk.Style()
style.configure('TButton', background='#e74c3c', foreground='white', font=('Arial', 12, 'bold'))
style.configure('TLabelFrame', background='#3498db', foreground='white', font=('Arial', 12, 'bold'))
style.configure('TLabel', background='#3498db', foreground='white', font=('Arial', 12))
style.map('TButton', background=[('active', '#d35400')])

frame = ttk.LabelFrame(app, text="Image Analysis", padding=(10, 5))
frame.pack(padx=10, pady=10, fill='both', expand=True)

img_path = 'C:/Users/user/Desktop/good.png'

def layout_ui_elements():
    # UI 요소 배치
    ttk.Label(frame, text="배율값:").pack(side=tk.LEFT, padx=5, pady=5)
    scale_factor_entry.pack(side=tk.LEFT, padx=5, pady=5)
    analyze_button.pack(side=tk.LEFT, padx=5, pady=5)

# UI 요소 생성 및 초기 배치
scale_factor_entry = ttk.Entry(frame)
scale_factor_entry.insert(0, "1.0")  # 기본값 설정

analyze_button = ttk.Button(frame, text="Analyze Image", command=on_analyze_button_click)

layout_ui_elements()

app.mainloop()
