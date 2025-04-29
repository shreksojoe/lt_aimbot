import csv
import tkinter as tk
from tkinter import filedialog

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")],
        title="Select a CSV File"
    )
    process_csv(file_path)

def process_csv(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
        
window = tk.Tk()
window.title("LT Aimbot")
# window.iconbitmap("")
window.geometry("450x150")

browse_button = tk.Button(window, text="Browse CSV", command=browse_file)
browse_button.pack(pady=50)

window.mainloop()
