# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect all dependencies for problematic packages
numpy_datas, numpy_binaries, numpy_hiddenimports = collect_all('numpy')
pandas_datas, pandas_binaries, pandas_hiddenimports = collect_all('pandas')
openpyxl_datas, openpyxl_binaries, openpyxl_hiddenimports = collect_all('openpyxl')

a = Analysis(
    ['src\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('src/instructions', 'instructions')] + numpy_datas + pandas_datas + openpyxl_datas,
    hiddenimports=[
        'psutil',
        'win32api',
        'win32con',
        'win32gui',
        'win32ui',
        'win32process',
        'win32com.client',
        'pyautogui',
        'keyboard',
        'pygetwindow',
        'json',
        'csv',
        'sys',
        'os',
        'time',
        're',
        'tkinter',
        'pymsgbox',
        'pytweening',
        'pyscreeze',
        'mouseinfo',
        'pyperclip',
        'pyrect',
        'win32gui',
        'win32con',
        'win32api',
        'pyautogui._pyautogui_win',
        'pyautogui._window_win',
        'pygetwindow._pygetwindow_win',
        'numpy',
        'pandas',
        'openpyxl',
        'et_xmlfile',
        'python-dateutil',
        'pytz',
        'tzdata',
        'six',
    ] + numpy_hiddenimports + pandas_hiddenimports + openpyxl_hiddenimports,
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add binaries
a.binaries += numpy_binaries + pandas_binaries + openpyxl_binaries

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
