@echo off
echo Building LT Aimbot executable...

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Install required dependencies if they don't exist
echo Installing required dependencies...
pip install psutil pywin32 openpyxl

REM Build the executable with PyInstaller
echo Building executable with PyInstaller...
python -m PyInstaller --clean --noconfirm --onefile ^
  --add-data "src/instructions;instructions" ^
  --hidden-import psutil ^
  --hidden-import keyboard ^
  --hidden-import numpy ^
  --hidden-import pandas ^
  --hidden-import pefile ^
  --hidden-import pywin32_ctypes ^
  --hidden-import pyautogui ^
  --hidden-import win32process ^
  --hidden-import win32api ^
  --hidden-import win32con ^
  --hidden-import pygetwindow ^
  --hidden-import openpyxl ^
  --hidden-import et_xmlfile ^
  src\main.py

echo Build complete! Executable is available in the dist folder.
pause
