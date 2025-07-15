# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files

# Path configurations
block_cipher = None
current_dir = os.path.abspath(SPECPATH)
hooks_dir = os.path.join(current_dir, 'hooks')

# Analysis configuration
a = Analysis(
    ['main.py'],
    pathex=[current_dir],
    binaries=[],
    datas=[('version.json', '.')],  # Include version.json at root level
    hiddenimports=[],
    hookspath=[hooks_dir] if os.path.exists(hooks_dir) else [],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest', 'unittest', 'doctest', 'pdb', 'tkinter.test', 'matplotlib', 'IPython', 'PIL.ImageQt'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ configuration (compressed Python modules)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE configuration
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # This makes it use one-folder mode
    name='lt_aimbot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip binaries to reduce size
    upx=True,    # Use UPX compression if available
    console=False,  # No console window (windowed mode)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add your .ico file path here if you have one
)

# COLLECT configuration for one-folder mode
# This creates a folder with all dependencies separate (not bundled into one exe)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='lt_aimbot',
)
