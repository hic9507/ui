import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import (Tk, Label, Button, Entry, Toplevel, filedialog, Scale,
                     HORIZONTAL, StringVar, Radiobutton)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

np.set_printoptions(threshold=np.inf, linewidth=np.inf)


class ImageUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Analysis")

        # In the __init__ method of ImageUI class, add:
        self.scale_label = Label(master=self.master, text="Scale Factor:")
        self.scale_label.grid(row=6, column=0)
        self.scale_entry = Entry(master=self.master)
        self.scale_entry.grid(row=6, column=1)

        # Control buttons
        self.start_button = Button(master=self.master, text="Start Inspection", command=self.load_video, width=11, height=2)
        self.start_button.grid(row=0, column=0)

        self.stop_button = Button(master=self.master, text="Stop Inspection", command=self.close, width=11, height=2)
        self.stop_button.grid(row=0, column=1)

        self.exit_button = Button(master=self.master, text="Exit", command=self.master.quit, width=11, height=2)
        self.exit_button.grid(row=0, column=2)

        # Inspection details
        self.item_label = Label(master=self.master, text="Item:")
        self.item_label.grid(row=1, column=0)
        self.item_entry = Entry(master=self.master)
        self.item_entry.grid(row=1, column=1)

        self.dimension_label = Label(master=self.master, text="Dimension:")
        self.dimension_label.grid(row=2, column=0)
        self.dimension_entry = Entry(master=self.master)
        self.dimension_entry.grid(row=2, column=1)

        self.tolerance_label = Label(master=self.master, text="Tolerance:")
        self.tolerance_label.grid(row=3, column=0)
        self.tolerance_entry = Entry(master=self.master)
        self.tolerance_entry.grid(row=3, column=1)

        self.defect_type = StringVar()
        self.defect_type.set("type1")
        defect_radiobutton1 = Radiobutton(master, text="Defect Type 1", variable=self.defect_type, value="type1")
        defect_radiobutton1.grid(row=4, column=0)
        defect_radiobutton2 = Radiobutton(master, text="Defect Type 2", variable=self.defect_type, value="type2")
        defect_radiobutton2.grid(row=4, column=1)

        # Sliders for adjusting defect detection sensitivity
        self.ng_count_slider = Scale(master, from_=0, to=100, orient=HORIZONTAL, label="NG Count")
        self.ng_count_slider.grid(row=5, column=0)

        self.threshold_slider = Scale(master, from_=0, to=255, orient=HORIZONTAL, label="Threshold")
        self.threshold_slider.grid(row=5, column=1)

        self.size_slider = Scale(master, from_=0, to=1000, orient=HORIZONTAL, label="Size")
        self.size_slider.grid(row=5, column=2)

    def process_image(self, frame):
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # _, binary_img = cv2.threshold(gray_img, 29, 255, cv2.THRESH_BINARY)
        _, binary_img = cv2.threshold(gray_img, 29, 255, cv2.THRESH_OTSU)
        binary_img = binary_img // 255

        kernel = np.ones((5, 5), np.uint8)
        filled_binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

        num_labels, labels = cv2.connectedComponents(filled_binary_img)

        area_count = np.bincount(labels.ravel())
        area_count[0] = 0
        largest_label = area_count.argmax()
        largest_component = (labels == largest_label).astype(np.uint8)

        contours, _ = cv2.findContours(largest_component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        epsilon = 0.01 * cv2.arcLength(contours[0], True)
        smoothed_contour = [cv2.approxPolyDP(contours[0], epsilon, True)]

        filled_img = cv2.drawContours(np.zeros_like(largest_component), smoothed_contour, -1, (1), thickness=cv2.FILLED)
        self.processed_img = filled_img * 255
        self.current_frame = frame

        # self.processed_img = binary_img
        # self.current_frame = frame

    def load_video(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open webcam!")
            return
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to fetch frame!")
            return
        self.process_image(frame)
        self.generate_graph()
        self.master.after(10, self.update_frame)

    def generate_graph(self):
        if not hasattr(self, 'processed_img') or not hasattr(self, 'current_frame'):
            return

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        plt.clf()

        fig = plt.figure(figsize=(12, 10))
        column_counts = [np.sum(self.processed_img[:, x] // 255) for x in range(self.processed_img.shape[1])]

        plt.subplot(2, 2, 1)
        plt.imshow(cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB))
        plt.title('Webcam Feed')

        plt.subplot(2, 2, 3)
        plt.imshow(self.processed_img, cmap='gray')
        plt.title('Processed Image')

        plt.subplot(2, 2, 2)
        plt.plot(column_counts)

        min_count = np.min(column_counts) - 1
        max_count = np.max(column_counts) + 1
        y_range = max_count - min_count
        y_padding = y_range * 0.1
        plt.ylim(min_count - y_padding, max_count + y_padding)

        plt.xlabel('x axis pixel')
        plt.ylabel('num of pixel is 1')
        plt.title('Pixel Distribution')

        plt.subplot(2, 2, 4)
        mean_count = np.mean(column_counts)
        std_dev = np.std(column_counts)
        scale_factor = float(self.scale_entry.get() or 1.0)
        mean_count *= scale_factor
        std_dev *= scale_factor

        plt.text(0.1, 0.6, f'Mean: {mean_count:.2f}', fontsize=14)
        plt.text(0.1, 0.4, f'Std Dev: {std_dev:.2f}', fontsize=14)
        plt.text(0.1, 0.2, f'Scale Factor: {scale_factor}', fontsize=14)
        plt.axis('off')

        plt.tight_layout()
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.5, wspace=0.5)

        self.canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.draw()
        # self.canvas.get_tk_widget().pack()
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=3)

    def close(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    root = Tk()
    app = ImageUI(root)
    root.mainloop()
