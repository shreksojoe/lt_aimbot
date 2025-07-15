import os
import sys
import shutil
import subprocess
import json

# Configuration
APP_NAME = "lt_aimbot"
MAIN_SCRIPT = "main.py"
VERSION_FILE = "version.json"
HOOKS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hooks")

def clean_build_directories():
    """Clean previous build directories"""
    print("Cleaning build directories...")
    
    # Get paths relative to this script
    dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
    build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
    
    # Clean dist directory
    app_dir = os.path.join(dist_dir, APP_NAME)
    if os.path.exists(app_dir):
        print(f"Removing {app_dir}")
        shutil.rmtree(app_dir)
    
    # Clean build directory
    if os.path.exists(build_dir):
        print(f"Removing {build_dir}")
        shutil.rmtree(build_dir)

def build_app():
    """Build the application using PyInstaller"""
    print("Building application with PyInstaller...")
    
    # Build the PyInstaller command
    cmd = [
        sys.executable,  # Use the current Python interpreter
        "-m",
        "PyInstaller",
        f"--name={APP_NAME}",
        "--onedir",      # Use one-folder mode
        "--windowed",    # Don't show console
        "--clean",       # Clean PyInstaller cache
        "--strip",       # Strip binaries
        "--exclude-module=pytest",
        "--exclude-module=unittest",
        "--exclude-module=doctest",
        "--exclude-module=pdb",
        "--exclude-module=tkinter.test",
        "--exclude-module=matplotlib",
        "--exclude-module=IPython",
        "--exclude-module=PIL.ImageQt",
        f"--add-data={VERSION_FILE}{os.pathsep}.",  # Add version.json to the build
    ]
    
    # Add hooks directory if it exists
    if os.path.exists(HOOKS_DIR):
        cmd.append(f"--additional-hooks-dir={HOOKS_DIR}")
    
    # Add the main script
    cmd.append(MAIN_SCRIPT)
    
    # Run PyInstaller
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"PyInstaller build failed with return code {result.returncode}")
        return False
    
    # Copy version.json to the build directory (to be extra sure)
    version_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), VERSION_FILE)
    if os.path.exists(version_file_path):
        dest_path = os.path.join("dist", APP_NAME, VERSION_FILE)
        print(f"Copying {VERSION_FILE} to {dest_path}")
        shutil.copy2(version_file_path, dest_path)
    
    return True

def get_app_size():
    """Calculate the size of the built application"""
    app_dir = os.path.join("dist", APP_NAME)
    total_size = 0
    file_count = 0
    
    for dirpath, dirnames, filenames in os.walk(app_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
            file_count += 1
    
    return total_size, file_count

def print_app_info():
    """Print information about the built application"""
    try:
        # Get version from version.json
        with open(VERSION_FILE, 'r') as f:
            version_data = json.load(f)
            version = version_data.get('version', 'unknown')
        
        # Get application size
        total_size, file_count = get_app_size()
        size_in_mb = total_size / (1024 * 1024)
        
        print("\n=== Application Build Summary ===")
        print(f"Application: {APP_NAME}")
        print(f"Version: {version}")
        print(f"Build Type: One-folder mode")
        print(f"Total Size: {size_in_mb:.2f} MB")
        print(f"File Count: {file_count}")
        print(f"Output Directory: {os.path.abspath(os.path.join('dist', APP_NAME))}")
        print("================================")
    except Exception as e:
        print(f"Error printing app info: {e}")

def main():
    """Main build function"""
    print(f"Starting build process for {APP_NAME}...")
    
    # Clean build directories
    clean_build_directories()
    
    # Build the app
    if build_app():
        print("\nBuild completed successfully!")
        print_app_info()
    else:
        print("\nBuild failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
