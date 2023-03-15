import ctypes
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import font
import os
import sys
import threading

stop_flag = False
background_thread = None

def background_change(path, num, seconds, filenames):
    while not stop_flag:
        x=0
        while True:
            x%=num-1
            x+=1
            
            print("Image =", x)
            WALLPAPER = path +"/"+ filenames[x]
            ctypes.windll.user32.SystemParametersInfoW(20,0,WALLPAPER)
            time.sleep(seconds)

def run_background_change(path, num, seconds, filenames):
    global background_thread
    if background_thread is None or not background_thread.is_alive():
        background_thread = threading.Thread(target=background_change, args=(path, num, seconds, filenames))
        background_thread.start()
    else:
        # Update the parameters of the existing thread
        background_thread._args = (path, num, seconds, filenames)

def count_items():
    # Open a file dialog to select a folder
    folder_path = filedialog.askdirectory()
    # If a folder was selected, count the number of files and directories in the folder
    if folder_path:
        num_files = 0
        num_dirs = 0

        for item in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, item)):
                num_files += 1
            else:
                num_dirs += 1

        file_names = []

        for file_name in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file_name)):
             file_names.append(file_name)

        print("Number of files in folder:", num_files)
        print("Number of directories in folder:", num_dirs)
        print(folder_path)
        print(file_names)
        run_background_change(folder_path, num_files, 10,file_names)

def restart_program():
     os.execv(sys.executable, ['python'] + sys.argv)

def exit_program():
    global stop_flag
    stop_flag = True
    window.destroy()
    sys.exit(0)


window = tk.Tk()
custom_font = font.Font(family="Helvetica", size=24, weight="bold")
normal_font = font.Font(family="Helvetica", size=12, weight="normal")
window.geometry("400x300")

title = tk.Label(text="WALLPAPER CHANGER\n******************\n", font=custom_font)
pre_info = tk.Label(text="Choose a folder full with images", font= normal_font)
title.pack()
pre_info.pack()
button = tk.Button(window, text="Open Folder", command=count_items)
button_restart = tk.Button(window,text="Restart", command=restart_program)
button_exit = tk.Button(window,text="Exit", command=exit_program)
button.pack()
button_restart.pack()
button_exit.pack()

window.mainloop()