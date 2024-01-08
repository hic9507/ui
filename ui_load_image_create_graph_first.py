import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Entry, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

np.set_printoptions(threshold=np.inf, linewidth=np.inf)


class ImageUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Analysis")

        self.label = Label(master, text="배율값을 입력하세요:", width=20, height=5, font=("Gulim", 14))
        self.label.pack()

        self.scale_entry = Entry(master, width=20, font=('Arial', 11))
        self.scale_entry.pack()
        self.scale_entry.insert(0, "1.0")

        self.load_button = Button(master, text="Load Image", command=self.load_image, width=11, height=2)
        self.load_button.pack()

        self.generate_button = Button(master, text="Generate Graph", command=self.generate_graph, width=11, height=2)
        self.generate_button.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        _, binary_img = cv2.threshold(self.img, 29, 255, cv2.THRESH_BINARY)
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

        self.processed_img = filled_img * 255
        print('image shape: ', self.processed_img.shape)

    def generate_graph(self):
        if not hasattr(self, 'img'):
            return

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        plt.clf()

        fig = plt.figure(figsize=(12, 10))
        column_counts = [np.sum(self.processed_img[:, x] // 255) for x in range(self.processed_img.shape[1])]

        plt.subplot(2, 2, 2)
        plt.plot(column_counts)
        plt.xlabel('x axis pixel')
        plt.ylabel('num of pixel is 1')
        plt.title('Pixel Distribution')

        plt.subplot(2, 2, 1)
        plt.imshow(self.img, cmap='gray')
        plt.title('Original Image')

        plt.subplot(2, 2, 3)
        plt.imshow(self.processed_img, cmap='gray')
        plt.title('Processed Image')

        plt.subplot(2, 2, 4)
        mean_count = np.mean(column_counts)
        std_dev = np.std(column_counts)
        scale_factor = float(self.scale_entry.get() or 1.0)
        mean_count *= scale_factor
        std_dev *= scale_factor

        plt.text(0.1, 0.6, f'Mean: {mean_count:.2f}', fontsize=12)
        plt.text(0.1, 0.4, f'Std Dev: {std_dev:.2f}', fontsize=12)
        plt.text(0.1, 0.2, f'Scale Factor: {scale_factor}', fontsize=12)
        plt.axis('off')

        plt.tight_layout()
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.5, wspace=0.5)

        self.canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = Tk()
    app = ImageUI(root)
    root.mainloop()
