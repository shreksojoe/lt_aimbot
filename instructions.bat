.\venv\Scripts\activate

pip install pyinstaller numpy pandas openpyxl

del build
del dist
del *.spec

pyinstaller --onefile src/main.py --distpath dist --clean --add-data "src/instructions;instructions"

.\venv\Scripts\pip install openpyxl

.\venv\Scripts\python -m PyInstaller --clean --noconfirm --onefile --add-data "src/instructions;instructions" --hidden-import psutil --hidden-import keyboard --hidden-import numpy --hidden-import pandas --hidden-import pefile --hidden-import pywin32_ctypes --hidden-import pyautogui --hidden-import win32process --hidden-import win32api --hidden-import win32con --hidden-import pygetwindow --hidden-import openpyxl --hidden-import et_xmlfile src\main.py
