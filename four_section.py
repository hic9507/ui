import tkinter as tk
from tkinter import ttk, Toplevel, Label, Button, Entry, Text
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Inspection UI")
        self.geometry("1200x900")

        self.cap = cv2.VideoCapture(0)
        self.mode = "작업자"

        self.mode_btn = tk.Button(self, text=self.mode, command=self.toggle_mode)
        self.mode_btn.grid(row=0, column=0, sticky='w')

        self.start_btn = tk.Button(self, text="Start", command=self.start_inspection)
        self.stop_btn = tk.Button(self, text="Stop", command=self.stop_inspection)
        self.exit_btn = tk.Button(self, text="Exit", command=self.quit)

        self.start_btn.grid(row=1, column=0, sticky='w')
        self.stop_btn.grid(row=1, column=1, sticky='w')
        self.exit_btn.grid(row=1, column=2, sticky='w')

        self.cam_img = tk.Label(self)
        self.cam_img.grid(row=2, column=0, sticky='w')

        self.scale_entry = Entry(self, width=20, font=('Arial', 11))
        self.scale_entry.grid(row=3, column=0)
        self.scale_entry.insert(0, "1.0")

        self.update_cam()
        self.after(10, self.generate_graph)

    def toggle_mode(self):
        if self.mode == "작업자":
            self.mode = "사용자"
            self.start_btn.config(text="IP Config", command=self.open_ip_and_settings)
        else:
            self.mode = "작업자"
            self.start_btn.config(text="Start", command=self.start_inspection)

        self.mode_btn.config(text=self.mode)

    def open_ip_and_settings(self):
        new_window = Toplevel(self)
        new_window.title("Settings and IP Configuration")

        labels = ["상부 외관", "하부 외관", "측면 치수"]
        for index, label_text in enumerate(labels):
            tk.Checkbutton(new_window, text=label_text).grid(row=index, column=0)
            tk.Entry(new_window, width=15).grid(row=index, column=1)
            tk.Checkbutton(new_window, text="검사 유무").grid(row=index, column=2)

            if label_text == "상부 외관":
                tk.Button(new_window, text="IP 불러오기").grid(row=index, column=3)
            elif label_text == "측면 치수":
                tk.Button(new_window, text="IP 저장하기").grid(row=index, column=3)

        tk.Label(new_window, text="Exposure Time(100~10000)").grid(row=4, column=0)
        tk.Entry(new_window, width=10).grid(row=4, column=1)
        tk.Button(new_window, text="적용").grid(row=4, column=2)

        tk.Label(new_window, text="Light Value(0~255)").grid(row=5, column=0)
        tk.Entry(new_window, width=10).grid(row=5, column=1)
        tk.Button(new_window, text="적용").grid(row=5, column=2)

        self.setting_cam_img = tk.Label(new_window)
        self.setting_cam_img.grid(row=6, column=0, columnspan=4)

        tk.Button(new_window, text="확인").grid(row=7, column=0)
        tk.Button(new_window, text="취소").grid(row=7, column=1)

        # self.update_setting_cam(new_window)

    # def update_setting_cam(self, window):
    #     ret, frame = self.cap.read()
    #     if ret:
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         frame = cv2.resize(frame, (320, 240))
    #         img = Image.fromarray(frame)
    #         imgtk = ImageTk.PhotoImage(image=img)
    #         self.setting_cam_img.imgtk = imgtk
    #         self.setting_cam_img.configure(image=imgtk)
    #
    #     window.after(10, lambda: self.update_setting_cam(window))

    def update_cam(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (320, 240))
            # img = Image.fromarray(frame)
            # imgtk = ImageTk.PhotoImage(image=img)
            # self.cam_img.imgtk = imgtk
            # self.cam_img.configure(image=imgtk)
            self.current_frame = frame
            self.process_image(frame)  # 원하는 경우 주석 처리하거나 제거할 수 있습니다.

        self.after(10, self.update_cam)

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

    def generate_graph(self):
        if not hasattr(self, 'processed_img') or not hasattr(self, 'current_frame'):
            return

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        plt.clf()

        fig = plt.figure(figsize=(12, 10))
        column_counts = [np.sum(self.processed_img[:, x] // 255) for x in range(self.processed_img.shape[1])]

        plt.subplot(2, 2, 1)
        # plt.imshow(cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB))
        plt.imshow(self.current_frame)
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

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=4)

        self.after(10, self.generate_graph)

    def start_inspection(self):
        pass

    def stop_inspection(self):
        pass

    def quit(self):
        self.cap.release()
        self.destroy()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
