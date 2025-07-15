import os
import sys
import shutil
import subprocess
import PyInstaller.__main__
from pathlib import Path

# Configuration
APP_NAME = "lt_aimbot"
MAIN_SCRIPT = "main.py"
ICON_FILE = None  # Set to path of .ico file if you have one

# Directory setup
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(ROOT_DIR, "dist")
BUILD_DIR = os.path.join(ROOT_DIR, "build")
HOOKS_DIR = os.path.join(ROOT_DIR, "hooks")
VERSION_FILE = os.path.join(ROOT_DIR, "version.json")

# Clean previous build
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

# Base PyInstaller arguments
pyinstaller_args = [
    MAIN_SCRIPT,
    '--name=%s' % APP_NAME,
    '--noconfirm',
    '--clean',
    # One-folder mode
    '--onedir',
    # Exclude console window
    '--windowed',
    # Add hooks directory
    '--additional-hooks-dir=%s' % HOOKS_DIR,
    # Optimize for size
    '--strip',
    # Exclude debug and test files
    '--exclude-module=pytest',
    '--exclude-module=unittest',
    '--exclude-module=doctest',
    '--exclude-module=pdb',
    # Explicit excludes to reduce size
    '--exclude-module=tkinter.test',
    '--exclude-module=matplotlib',
    '--exclude-module=IPython',
    '--exclude-module=PIL.ImageQt',
    # Other obfuscation options (compatible with PyInstaller 6.0+)
    '--hide-console=hide-early',
]

# Add icon if available
if ICON_FILE and os.path.exists(ICON_FILE):
    pyinstaller_args.append('--icon=%s' % ICON_FILE)

# Add version file
if os.path.exists(VERSION_FILE):
    pyinstaller_args.append('--add-data=%s%s%s' % (VERSION_FILE, os.pathsep, '.'))

# Execute PyInstaller
print("Building application with PyInstaller...")
PyInstaller.__main__.run(pyinstaller_args)

# Copy version.json to dist folder
if os.path.exists(VERSION_FILE):
    shutil.copy2(VERSION_FILE, os.path.join(DIST_DIR, APP_NAME))

print(f"\nBuild completed! Output in {os.path.join(DIST_DIR, APP_NAME)}")
