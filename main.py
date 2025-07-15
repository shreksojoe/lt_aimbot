import sys
import os
import subprocess
import threading
import time
import ctypes
from pathlib import Path

# Check if this is running from the installed location or development environment
def is_frozen():
    """Determine if running from PyInstaller executable or in development"""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def get_app_dir():
    """Get the application directory based on whether we're frozen or not"""
    if is_frozen():
        # If running as PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        # If running in development mode
        return os.path.dirname(os.path.abspath(__file__))

def check_for_updates_async():
    """Check for updates in a separate thread"""
    try:
        app_dir = get_app_dir()
        # Look for updater in multiple locations based on one-folder structure
        updater_exe_paths = [
            os.path.join(app_dir, "updater", "updater.exe"),  # One-folder mode
            os.path.join(app_dir, "updater.exe"),             # Legacy one-file mode
            os.path.join(app_dir, "updater.lnk")              # Shortcut to updater
        ]
        
        updater_py = os.path.join(app_dir, "src", "updater.py")
        
        # If we're running the installed version, find and use the updater
        if is_frozen():
            for updater_path in updater_exe_paths:
                if os.path.exists(updater_path):
                    # Use safer method to start process
                    os.startfile(updater_path, "--silent")
                    return
        
        # If in development or updater.exe doesn't exist yet, use Python script
        if os.path.exists(updater_py):
            # Use safer method to avoid Windows Defender triggers
            if hasattr(os, "spawnl"):
                os.spawnl(os.P_NOWAIT, sys.executable, sys.executable, updater_py, "--silent")
            else:
                subprocess.Popen([sys.executable, updater_py, "--silent"], 
                               creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"Error checking for updates: {e}")

def show_update_dialog():
    """Show a dialog asking if the user wants to check for updates"""
    # Check for a file that indicates this is the first run after installation
    first_run_file = os.path.join(get_app_dir(), "first_run")
    
    if os.path.exists(first_run_file):
        # Delete the first run file
        try:
            os.remove(first_run_file)
        except:
            pass
            
        # Show a welcome message
        ctypes.windll.user32.MessageBoxW(0, 
            "Thank you for installing LT Aimbot!\n\nThe application will automatically check for updates at startup.", 
            "Welcome", 0x40)

def main():
    """Main application entry point"""
    # Check for updates in the background
    update_thread = threading.Thread(target=check_for_updates_async)
    update_thread.daemon = True
    update_thread.start()
    
    # Show first-run dialog if needed
    show_update_dialog()
    
    # Import the actual application module
    # We import here to ensure update checking happens before app initialization
    from src import xlsx_to_csv
    
    # Get command-line arguments, if any
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # If a file was provided as argument, process it
    if args and os.path.isfile(args[0]):
        xlsx_to_csv.main(args[0])
    else:
        # Show a simple GUI to select a file if no argument was provided
        import tkinter as tk
        from tkinter import filedialog, messagebox
        
        def select_file():
            file_path = filedialog.askopenfilename(
                title="Select Excel File",
                filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")]
            )
            if file_path:
                result = xlsx_to_csv.main(file_path)
                if result.endswith('.csv'):
                    messagebox.showinfo("Success", f"File converted successfully to {result}")
                else:
                    messagebox.showerror("Error", f"Failed to convert file")
                root.destroy()
        
        root = tk.Tk()
        root.title("LT Aimbot - Excel to CSV Converter")
        root.geometry("400x200")
        root.resizable(False, False)
        
        # Center window
        root.eval('tk::PlaceWindow . center')
        
        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        label = tk.Label(frame, text="Welcome to LT Aimbot Excel to CSV Converter", font=("Arial", 12))
        label.pack(pady=10)
        
        instruction = tk.Label(frame, text="Click the button below to select an Excel file to convert")
        instruction.pack(pady=5)
        
        select_btn = tk.Button(frame, text="Select Excel File", command=select_file, width=20, height=2)
        select_btn.pack(pady=10)
        
        # Add a "Check for Updates" button
        def check_for_updates():
            app_dir = get_app_dir()
            
            # Look for updater in multiple locations based on one-folder structure
            updater_exe_paths = [
                os.path.join(app_dir, "updater", "updater.exe"),  # One-folder mode
                os.path.join(app_dir, "updater.exe"),             # Legacy one-file mode
                os.path.join(app_dir, "updater.lnk")              # Shortcut to updater
            ]
            
            updater_py = os.path.join(app_dir, "src", "updater.py")
            
            # Try to use the updater executable first
            if is_frozen():
                for updater_path in updater_exe_paths:
                    if os.path.exists(updater_path):
                        # Use safer method to start process
                        os.startfile(updater_path)
                        return
            
            # Fall back to Python script if needed
            if os.path.exists(updater_py):
                if hasattr(os, "spawnl"):
                    os.spawnl(os.P_NOWAIT, sys.executable, sys.executable, updater_py)
                else:
                    # Only use subprocess if os.spawnl isn't available
                    subprocess.Popen([sys.executable, updater_py], 
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        
        update_btn = tk.Button(frame, text="Check for Updates", command=check_for_updates, width=15)
        update_btn.pack(side=tk.BOTTOM, pady=5)
        
        root.mainloop()

if __name__ == "__main__":
    main()
