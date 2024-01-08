import tkinter as tk
from tkinter import ttk, Toplevel
from PIL import Image, ImageTk
import cv2


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

        self.bin_img = tk.Label(self)
        self.bin_img.grid(row=2, column=1, sticky='w')

        self.item_label = tk.Label(self, text="검사 품목 선택")
        self.item_label.grid(row=7, column=3, sticky='w')
        self.items = ttk.Combobox(self, values=["Window", "Bolt", "Nut"])
        self.items.grid(row=7, column=4, sticky='w')

        self.variations = ['A', 'B', 'C', 'D']
        self.entries = {}

        for i in range(3, 10):
            self.grid_columnconfigure(i, minsize=50)

        settings = ["개수", "임계값", "크기"]

        for index, var in enumerate(self.variations, start=8):
            label = tk.Label(self, text=f"{var}:")
            label.grid(row=index, column=3, sticky='w')
            entry_val = tk.Entry(self, width=10)
            entry_val.grid(row=index, column=4, sticky='w')
            sign_label = tk.Label(self, text="±")
            sign_label.grid(row=index, column=5, sticky='w')
            tolerance_entry = tk.Entry(self, width=10)
            tolerance_entry.grid(row=index, column=6, sticky='w')
            self.entries[var] = (entry_val, tolerance_entry)

        for i, setting in enumerate(settings, start=8):
            setting_label = tk.Label(self, text=setting)
            setting_label.grid(row=i, column=7, sticky='w')
            trackbar = ttk.Scale(self, from_=0, to_=100, orient="horizontal")
            trackbar.grid(row=i, column=8, sticky='w')

        self.defect_labels = ['불량 종류', '불량 시점', '불량 시간 관리']
        for idx, label_text in enumerate(self.defect_labels, start=len(self.variations) + 8):
            label = tk.Label(self, text=label_text)
            label.grid(row=idx, column=3, sticky='w')
            entry = tk.Entry(self, width=20)
            entry.grid(row=idx, column=4, columnspan=2, sticky='w')

        self.log_label = tk.Label(self, text="외관 검사 결과 및 치수 검사 로그")
        self.log_label.grid(row=8, column=0, columnspan=2)
        self.log_text = tk.Text(self, height=20, width=100)
        self.log_text.grid(row=9, column=0, columnspan=2, rowspan=5)

        self.update_cam()

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
            frame = cv2.resize(frame, (320, 240))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.cam_img.imgtk = imgtk
            self.cam_img.configure(image=imgtk)

        self.after(10, self.update_cam)

    def update_setting_cam(self, window):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (320, 240))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.setting_cam_img.imgtk = imgtk
            self.setting_cam_img.configure(image=imgtk)

        window.after(10, lambda: self.update_setting_cam(window))

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
