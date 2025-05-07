import subprocess
import platform

# Your main script
entry_script = "ui.py"

# Files or folders to include: (source, destination in bundle)
data_files = [
    ("login.py", "."),
    ("process_csv.py", "."),
    ("json_gps.py", "."),
    ("address_search.py", "."),
    ("home_btn.json", "data"),
    ("login_credentials.json", "data"),
    ("ticket.json", "data")
]

# Choose separator based on OS
sep = ";" if platform.system() == "Windows" else ":"

# Build the --add-data args
add_data_args = []
for src, dest in data_files:
    add_data_args.append(f"--add-data={src}{sep}{dest}")

# PyInstaller command
command = [
    "pyinstaller",
    "--onefile",
    *add_data_args,
    entry_script
]

# Run the command
print("Running PyInstaller...")
result = subprocess.run(command)

if result.returncode == 0:
    print("✅ Build completed. Check the 'dist/' folder.")
else:
    print("❌ Build failed.")
