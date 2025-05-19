import tempfile
import shutil
import atexit
import os
import csv
import sys
import tkinter as tk
from tkinter import filedialog
import login
import process_csv


tmp_file_path = None

# browse file manager
def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")],
        title="Select a CSV File"
    )
    tmp_file_path = file_path

    if tmp_file_path != '':
        window.destroy()
        login.to_Label_Traxx()
        process_csv.start(tmp_file_path)

# convert csv to 2d List
def csv_converter(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        order = list(reader)
        return order
        
# makes temporary duplicate of json file
def file_dup(path):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    temp_path = temp_file.name
    temp_file.close()

    shutil.copy2(str(path), str(temp_path))
    return temp_path

def create_window():
    print("ui.py started, print works")
    window = tk.Tk()
    window.title("LT Aimbot")
    #window.iconbitmap("coding_dino.ico")
    window.geometry("450x150")

    browse_button = tk.Button(window, text="Browse CSV", command=browse_file)
    browse_button.pack(pady=50)
    
    window.mainloop()
    return tmp_file_path
   

