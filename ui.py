import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def analyze_image(img_path, scale_factor=1.0):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    _, binary_img = cv2.threshold(img, 29, 255, cv2.THRESH_BINARY)
    binary_img = binary_img // 255

    width = binary_img.shape[1]
    step_size = 1
    column_counts = [np.sum(binary_img[:, x:x + step_size]) for x in range(0, width, step_size)]

    fig = plt.figure(figsize=(20, 20))

    plt.subplot(2, 2, 2)
    plt.plot(column_counts)
    plt.xlabel('x axis pixel')
    plt.ylabel('num of pixel is 1')
    plt.title('Pixel Distribution')

    plt.subplot(2, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')

    plt.subplot(2, 2, 3)
    plt.imshow(binary_img, cmap='gray')
    plt.title('Binary Image')

    plt.subplot(2, 2, 4)
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


app = tk.Tk()
app.title("Image Analyzer")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

img_path = 'C:/Users/user/Desktop/good.png'

scale_factor = float(input("배율값 입력: ") or 1.0)

fig = analyze_image(img_path, scale_factor)
if fig:
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()

app.mainloop()
