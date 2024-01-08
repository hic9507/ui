import tkinter as tk
from tkinter import ttk, simpledialog, Scale

root = tk.Tk()
root.title("Main Application")

def create_worker_panel():
    worker_frame = ttk.Frame(root)
    worker_frame.grid(row=1, column=0, columnspan=2, sticky='w')

    # Worker controls
    start_button = ttk.Button(worker_frame, text="START")
    start_button.pack(side="left")

    stop_button = ttk.Button(worker_frame, text="STOP")
    stop_button.pack(side="left")

    exit_button = ttk.Button(worker_frame, text="EXIT")
    exit_button.pack(side="left")

    return worker_frame

def create_user_panel():
    user_frame = ttk.Frame(root)
    user_frame.grid(row=1, column=0, columnspan=2, sticky='w')

    # User controls
    ipconfig_button = ttk.Button(user_frame, text="IPCONFIG", command=create_ipconfig_dialog)
    ipconfig_button.pack(side="left")

    cam_calibration_button = ttk.Button(user_frame, text="CAM CALIBRATION")
    cam_calibration_button.pack(side="left")

    load_model_button = ttk.Button(user_frame, text="LOAD MODEL")
    load_model_button.pack(side="left")

    load_db_button = ttk.Button(user_frame, text="LOAD DATABASE")
    load_db_button.pack(side="left")

    return user_frame

def create_ipconfig_dialog():
    ipconfig_dialog = simpledialog.Dialog(root, "IP Configuration")

    # ... Implement the contents of this dialog

def open_worker():
    user_panel.grid_remove()
    worker_panel.grid()

def open_user():
    worker_panel.grid_remove()
    user_panel.grid()

worker_button = ttk.Button(root, text="작업자", command=open_worker)
worker_button.grid(row=0, column=0)

user_button = ttk.Button(root, text="사용자", command=open_user)
user_button.grid(row=0, column=1)

# Create panels but do not show them yet
worker_panel = create_worker_panel()
user_panel = create_user_panel()

# Initially show worker panel
worker_panel.grid()
user_panel.grid_remove()

root.mainloop()
