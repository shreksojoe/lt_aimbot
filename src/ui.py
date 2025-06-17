import tempfile
import shutil
import atexit
import os
import csv
import sys
import tkinter as tk
from tkinter import filedialog
import open_files
import process_csv
import xlsx_to_csv


tmp_file_paths = None

# browse file manager
def browse_files(window):
    try:
        # Open file dialog to select CSV files
        file_paths = filedialog.askopenfilenames(
            title="Select CSV File(s)",
            filetypes=[ ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx"),
            ("All Supported Files", "*.csv *.xlsx"),
            ("All Files", "*.*")]
        )
        
        # Convert to list
        file_paths = list(file_paths)
        print(f"Selected files: {file_paths}")

        # If no files are selected, return early
        if not file_paths:
            print("No files selected. Please try again.")
            return None
        
        # Store the file paths in the global variable
        global tmp_file_paths
        tmp_file_paths = file_paths
        
        # Close the window and proceed with processing
        window.destroy()

        # Process each file (CSV or Excel)
        processed_files = []
        for file in tmp_file_paths:
            # Check if the file is an Excel file
            if file.lower().endswith('.xlsx'):
                try:
                    # Convert Excel to CSV
                    csv_file = xlsx_to_csv.convert(file)
                    # Process the converted CSV file
                    open_files.open_csv_file(csv_file)
                    processed_files.append(csv_file)
                except Exception as e:
                    print(f"Error converting Excel file {file}: {e}")
            else:
                # Process CSV file directly
                open_files.open_csv_file(file)
                processed_files.append(file)
        
        # Update tmp_file_paths with processed files (including converted ones)
        tmp_file_paths = processed_files

        return tmp_file_paths

    except Exception as e:
        print(f"Error in browse_files: {e}")
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
                                  command=lambda: browse_files(window))
        browse_button.pack(pady=50)
        
        # launch window
        window.mainloop()
        return tmp_file_paths

    except Exception as e:
        print(f"Error in create_window: {e}")
        raise

