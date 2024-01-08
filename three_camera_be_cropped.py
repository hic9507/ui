import tkinter as tk
from tkinter import ttk, Toplevel, Label, Button, Entry, Text
from PIL import Image, ImageTk
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Inspection UI")
        self.geometry("1500x900")

        self.label = Label(master=self.master, text="배율값을 입력하세요:", width=20, height=2, font=("Arial", 14))
        self.label.grid(row=3, column=0, sticky='w')

        self.scale_entry = Entry(self, width=20, font=('Arial', 11))
        self.scale_entry.grid(row=3, column=1)
        self.scale_entry.insert(0, "1.0")

        self.cap = cv2.VideoCapture(0)
        self.mode = "작업자"

        self.mode_btn = tk.Button(self, text=self.mode, command=self.toggle_mode, font=('Arial', 11))
        self.mode_btn.grid(row=0, column=0, sticky='w')

        self.start_btn = tk.Button(self, text="Start", command=self.start_inspection, font=('Arial', 11))
        self.stop_btn = tk.Button(self, text="Stop", command=self.stop_inspection, font=('Arial', 11))
        self.exit_btn = tk.Button(self, text="Exit", command=self.quit, font=('Arial', 11))

        self.start_btn.grid(row=1, column=0, sticky='w', columnspan=2)
        self.stop_btn.grid(row=1, column=1, sticky='w', columnspan=2)
        self.exit_btn.grid(row=1, column=2, sticky='w', columnspan=2)

        # self.start_btn.grid(row=1, column=0, sticky='w', padx=(0, 5), pady=5)  # 5 pixel padding to the right
        # self.stop_btn.grid(row=1, column=1, sticky='w', padx=(0, 5), pady=5)   # 5 pixel padding to the right
        # self.exit_btn.grid(row=1, column=2, sticky='w', padx=(0, 5), pady=5)   # 5 pixel padding to the right


        self.cam_img = tk.Label(self)
        self.cam_img.grid(row=2, column=0, sticky='w')

        self.bin_img = tk.Label(self)
        self.bin_img.grid(row=2, column=1, sticky='w')

        self.item_label = tk.Label(self, text="검사 품목 선택", font=("Arial", 14))
        self.item_label.grid(row=80, column=1, sticky='w')
        self.items = ttk.Combobox(self, values=["Window", "Bolt", "Nut"])
        self.items.grid(row=81, column=1, sticky='w')

        self.variations = ['A', 'B', 'C', 'D']
        self.entries = {}

        for i in range(3, 10):
            self.grid_columnconfigure(i, minsize=10)

        settings = ["개수", "임계값", "크기"]

        for index, var in enumerate(self.variations, start=82):
            label = tk.Label(self, text=f"{var}:", width=5, font=("Arial", 14))
            label.grid(row=index, column=1, sticky='w', padx=2, pady=2)
            entry_val = tk.Entry(self, width=12)
            entry_val.grid(row=index, column=2, sticky='w', padx=2, pady=2)
            sign_label = tk.Label(self, text="±", padx=0, pady=0, font=("Arial", 14))
            sign_label.grid(row=index, column=3, sticky='w', padx=2)
            tolerance_entry = tk.Entry(self, width=5)
            tolerance_entry.grid(row=index, column=4, sticky='w', padx=2, pady=2)
            self.entries[var] = (entry_val, tolerance_entry)

        for i, setting in enumerate(settings, start=82):
            setting_label = tk.Label(self, text=setting, font=("Arial", 14))
            setting_label.grid(row=i, column=5, sticky='e', padx=(20, 0))
            trackbar = ttk.Scale(self, from_=0, to_=100, orient="horizontal")
            trackbar.grid(row=i, column=6, sticky='w')

        self.defect_labels = ['불량 종류', '불량 시점', '불량 시간 관리']
        for idx, label_text in enumerate(self.defect_labels, start=len(self.variations) + 83):
            label = tk.Label(self, text=label_text, font=("Arial", 14))
            label.grid(row=idx, column=1, sticky='w')
            entry = tk.Entry(self, width=20)
            entry.grid(row=idx, column=2, columnspan=2, sticky='w')

        self.log_label = tk.Label(self, text="외관 검사 결과 및 치수 검사 로그", font=("Arial", 14))
        self.log_label.grid(row=80, column=0, columnspan=1)
        self.log_text = tk.Text(self, height=20, width=80)
        self.log_text.grid(row=81, column=0, columnspan=1, rowspan=5)

        self.update_cam()
        self.generate_graph()


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

        self.update_setting_cam(new_window)

    def update_cam(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            # img = Image.fromarray(frame)
            # imgtk = ImageTk.PhotoImage(image=img)
            # self.cam_img.imgtk = imgtk
            # self.cam_img.configure(image=imgtk)
            self.process_image(frame)  # 원하는 경우 주석 처리하거나 제거.


        self.after(10, self.update_cam)

    def update_setting_cam(self, window):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.setting_cam_img.imgtk = imgtk
            self.setting_cam_img.configure(image=imgtk)
            self.current_frame = frame
            self.process_image(self.current_frame)  # 원하는 경우 주석 처리하거나 제거.

        window.after(10, lambda: self.update_setting_cam(window))

    def start_inspection(self):
        pass

    def stop_inspection(self):
        pass

    def process_image(self, frame):
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary_img = cv2.threshold(gray_img, 29, 255, cv2.THRESH_OTSU)
        # binary_img = cv2.resize(binary_img, (224, 224))
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
        self.current_frame = frame  # 원래
        # self.current_frame = cv2.resize(frame, (224, 224))

    def generate_graph(self):
        # 기존에 캔버스가 생성되었다면 파괴합니다.
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        plt.clf()

        fig = plt.figure(figsize=(20, 5))
        column_counts = [np.sum(self.processed_img[:, x] // 255) for x in range(self.processed_img.shape[1])]

        plt.subplot(2, 3, 1)
        plt.imshow(self.current_frame)
        plt.title('Webcam Feed')

        plt.subplot(2, 3, 2)
        plt.imshow(self.current_frame)
        plt.title('Webcam Feed2')

        plt.subplot(2, 3, 3)
        plt.imshow(self.current_frame)
        plt.title('Webcam Feed3')

        plt.subplot(2, 3, 4)
        plt.imshow(self.processed_img, cmap='gray')
        plt.title('Processed Image')

        plt.subplot(2, 3, 5)
        plt.plot(column_counts)

        min_count = np.min(column_counts) - 1
        max_count = np.max(column_counts) + 1
        y_range = max_count - min_count
        y_padding = y_range * 0.1
        plt.ylim(min_count - y_padding, max_count + y_padding)

        plt.xlabel('x axis pixel')
        plt.ylabel('num of pixel is 1')
        plt.title('Pixel Distribution')

        plt.subplot(2, 3, 6)
        mean_count = np.mean(column_counts)
        std_dev = np.std(column_counts)
        scale_factor = float(self.scale_entry.get() or 1.0)
        mean_count *= scale_factor
        std_dev *= scale_factor

        plt.text(0.1, 0.6, f'Mean: {mean_count:.2f}', fontsize=14)
        plt.text(0.1, 0.4, f'Std Dev: {std_dev:.2f}', fontsize=14)
        plt.text(0.1, 0.2, f'Scale Factor: {scale_factor}', fontsize=14)
        plt.axis('off')

        plt.tight_layout(w_pad=-1, h_pad=-1)
        # plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.2, wspace=0.1)
        # plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, hspace=0.1, wspace=0.1)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.5, wspace=0.5)   # 원본

        # plt.subplots_adjust(hspace=0, wspace=0)

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=4)

        # 주기적으로 그래프를 업데이트하려면 아래 코드를 사용합니다.
        self.after(1000, self.generate_graph)
        plt.close()

    def quit(self):
        self.cap.release()
        self.destroy()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
