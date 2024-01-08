import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

def video_stream():
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()  # 웹캠에서 이미지 캡쳐
    frame = cv2.resize(frame, (300, 200))  # 웹캠 크기 조절
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.config(image=imgtk)
    lmain.after(10, video_stream)

root = tk.Tk()                  # 윈도우 이름 = tkinter.Tk() 가장 상위 레벨의 윈도우 창 생성
root.title("Main Application")

# 작업자 및 사용자 버튼을 보관하는 프레임
selection_frame = ttk.Frame(root)
selection_frame.pack(pady=20)

# 작업자 및 사용자 패널용 프레임
worker_frame = ttk.Frame(root)
user_frame = ttk.Frame(root)

def create_worker_panel():
    ttk.Button(worker_frame, text="START").pack(side="left", padx=5)
    ttk.Button(worker_frame, text="STOP").pack(side="left", padx=5)
    ttk.Button(worker_frame, text="EXIT").pack(side="left", padx=5)

def create_user_panel():
    ttk.Button(user_frame, text="IPCONFIG").pack(side="left", padx=5)
    ttk.Button(user_frame, text="CAM CALIBRATION").pack(side="left", padx=5)
    ttk.Button(user_frame, text="LOAD MODEL").pack(side="left", padx=5)
    ttk.Button(user_frame, text="LOAD DATABASE").pack(side="left", padx=5)

def show_worker_panel():
    user_frame.pack_forget()  # 사용자 프레임 감추기
    worker_frame.pack(pady=20)  # 작업자 프레임 보이기

def show_user_panel():
    worker_frame.pack_forget()  # 작업자 프레임 감추기
    user_frame.pack(pady=20)  # 사용자 프레임 보이기

# 작업자-사용자 선택 버튼 생성
ttk.Button(selection_frame, text="작업자", command=show_worker_panel).pack(side="left", padx=10)
ttk.Button(selection_frame, text="사용자", command=show_user_panel).pack(side="left", padx=10)

# 작업자 및 사용자 패널을 생성하지만 아직 표시하지 않음
create_worker_panel()
create_user_panel()

root.mainloop()         # 윈도우 이름.mainloop()를 사용해 윈도우 이름의 윈도우 창을 윈도우가 종료될 때까지 실행시킴
