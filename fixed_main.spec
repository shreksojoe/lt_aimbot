# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all data files for numpy and pandas
datas = [
    ('src/instructions', 'instructions'),
]

# Add all numpy and pandas submodules
a = Analysis(
    ['src\\main_fixed.py'],
    pathex=['src'],
    binaries=[],
    datas=datas,
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
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add pandas and numpy data files
a.datas += collect_data_files('numpy')
a.datas += collect_data_files('pandas')
a.datas += collect_data_files('openpyxl')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
