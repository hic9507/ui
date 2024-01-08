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
        print(self.img.shape)

    def generate_graph(self):
        if not hasattr(self, 'img'):
            return
        out = open('output.text', 'w')
        # 이전의 그래프가 있으면 제거
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
        plt.clf()

        # 그래프 생성
        fig = plt.figure(figsize=(12, 10))
        _, binary_img = cv2.threshold(self.img, 29, 255, cv2.THRESH_BINARY)
        # print('binary_img', '\n', binary_img[::])
        binary_img = binary_img // 255
        print('binary_img', '\n', binary_img, file=out)


        column_counts = [np.sum(binary_img[:, x]) for x in range(binary_img.shape[1])]

        plt.subplot(2, 2, 2)
        plt.plot(column_counts)
        plt.xlabel('x axis pixel')
        plt.ylabel('num of pixel is 1')
        plt.title('Pixel Distribution')

        plt.subplot(2, 2, 1)
        plt.imshow(self.img, cmap='gray')
        plt.title('Original Image')

        plt.subplot(2, 2, 3)
        plt.imshow(binary_img, cmap='gray')
        plt.title('Binary Image')

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

        # 마진 조절
        plt.tight_layout()
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.5, wspace=0.5)

        # Plot을 Tkinter에 삽입
        self.canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = Tk()
    app = ImageUI(root)
    root.mainloop()
