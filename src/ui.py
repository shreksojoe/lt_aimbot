import tempfile
import shutil
import atexit
import os
import csv
import sys
import tkinter as tk
import open_files
from tkinter import filedialog
import process_csv


tmp_file_path = None

# browse file manager
def browse_file(window):
    try:
        # Open file dialog to select a CSV file
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")],
            title="Select a CSV File"
        )
        
        # If no file is selected, return early
        if not file_path or file_path == '':
            print("No file selected. Please try again.")
            return
            
        
        # Store the file path in the global variable
        global tmp_file_path
        tmp_file_path = file_path
        
        # Close the window and proceed with processing
        window.destroy()

        # Process the CSV file
        open_files.open_csv_file(tmp_file_path)
        return tmp_file_path

    except Exception as e:
        print(f"Error in browse_file: {e}")
        # Optionally, show an error message to the user
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", f"Failed to process the file: {e}")

        
# makes temporary duplicate of json file

def create_window():
    try:
        # creates window
        window = tk.Tk()
        window.title("LT Aimbot")
        #window.iconbitmap("coding_dino.ico")
        window.geometry("450x150")
        
        # Brings window to the front
        window.lift()
        window.attributes('-topmost', True)
        window.after_idle(window.attributes, '-topmost', False)
        
        # Make Button
        browse_button = tk.Button(window, text="Browse CSV",
                                  command=lambda: browse_file(window))
        browse_button.pack(pady=50)
        
        # launch window
        window.mainloop()
        return tmp_file_path

    except Exception as e:
        print(f"Error in create_window: {e}")
        raise
