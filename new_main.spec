# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

datas = [('src/instructions', 'instructions')] + collect_data_files('numpy') + collect_data_files('pandas')

# Add all numpy and pandas submodules
numpy_imports = collect_submodules('numpy')
pandas_imports = collect_submodules('pandas')

a = Analysis(
    ['src\\main.py'],
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
        'numpy.core',
        'numpy.core._dtype_ctypes',
        'numpy.core._methods',
        'numpy.lib.format',
        'pandas.core',
        'pandas.io.formats',
        'pandas.io.excel',
        'openpyxl'
    ] + numpy_imports + pandas_imports,
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,

)

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
