import tempfile
import shutil
import atexit
import subprocess
import os
import csv
import tkinter as tk
from tkinter import filedialog


global tmp_file_path

# browse file manager
def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")],
        title="Select a CSV File"
    )
    tmp_file_path = file_path

    if tmp_file_path != '':
        window.destroy()
        login = "login.py"
        subprocess.run(["python", login])
        process_csv = "process_csv.py"
        subprocess.run(["python", process_csv, tmp_file_path])


# convert csv to 2d List
def process_csv(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        order = list(reader)
        return order
        
# makes temporary duplicate of json file
def file_dup(path):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    temp_path = temp_file.name
    temp_file.close()

    shutil.copy2(path, temp_path)
    return temp_path

if __name__ == "__main__":
    window = tk.Tk()
    window.title("LT Aimbot")
    # window.iconbitmap("")
    window.geometry("450x150")

    browse_button = tk.Button(window, text="Browse CSV", command=browse_file)
    browse_button.pack(pady=50)
    
    window.mainloop()
   
