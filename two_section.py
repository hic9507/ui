import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Inspection UI")
        self.geometry("1200x900")

        self.cap = cv2.VideoCapture(0)
        self.mode = "작업자"  # Operator or User

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
        for i in range(3, 7):  # 3부터 6까지의 열에 대해서
            self.grid_columnconfigure(i, minsize=100)  # 최소 폭을 50으로 설정. 이 값을 조절하여 원하는 간격을 얻을 수 있습니다.

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

        self.log_label = tk.Label(self, text="외관 검사 결과 및 치수 검사 로그")
        self.log_label.grid(row=7, column=0, columnspan=2)
        self.log_text = tk.Text(self, height=20, width=100)
        self.log_text.grid(row=8, column=0, columnspan=2, rowspan=5)

        self.update_cam()

    def toggle_mode(self):
        if self.mode == "작업자":
            self.mode = "사용자"
            self.start_btn.config(text="IP Config")
            self.stop_btn.config(text="Cam Calibration")
            self.exit_btn.config(text="Load Model")
            self.load_db_btn = tk.Button(self, text="데이터베이스 로드")
            self.load_db_btn.grid(row=1, column=3, sticky='w')
        else:
            self.mode = "작업자"
            self.start_btn.config(text="Start")
            self.stop_btn.config(text="Stop")
            self.exit_btn.config(text="Exit")
            self.load_db_btn.destroy()
        self.mode_btn.config(text=self.mode)

    def update_cam(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (320, 240))
            im = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=im)
            self.cam_img.imgtk = imgtk
            self.cam_img.configure(image=imgtk)

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)
            binary_frame = cv2.resize(binary_frame, (320, 240))
            bin_im = Image.fromarray(binary_frame)
            bin_imgtk = ImageTk.PhotoImage(image=bin_im)
            self.bin_img.imgtk = bin_imgtk
            self.bin_img.configure(image=bin_imgtk)

        self.cam_img.after(10, self.update_cam)

    def start_inspection(self):
        print("검사 시작")

    def stop_inspection(self):
        print("검사 중단")

    def quit(self):
        self.cap.release()
        self.destroy()

app = Application()
app.mainloop()
