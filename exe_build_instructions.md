# Instructions for Building Python Executable with PyInstaller

This guide provides step-by-step instructions for creating an executable from a Python project using PyInstaller, with specific focus on projects using PyAutoGUI and other GUI-related libraries.

## Step 1: Install Dependencies

First, activate your virtual environment if you have one, then install the required dependencies:

```powershell
.\.venv\Scripts\pip install pywin32
.\.venv\Scripts\pip install psutil
.\.venv\Scripts\pip install pyautogui==0.9.50  # Using this specific version for stability
```

## Step 2: Create PyAutoGUI Hook

Create a `hooks` directory in your project root if it doesn't exist, then create a file `hooks/hook-pyautogui.py` with the following content:

```python
from PyInstaller.utils.hooks import collect_all, collect_submodules

datas, binaries, hiddenimports = collect_all('pyautogui')

# Add all submodules
hiddenimports += collect_submodules('pyautogui')
hiddenimports += collect_submodules('pygetwindow')
hiddenimports += collect_submodules('win32gui')
hiddenimports += collect_submodules('win32api')
hiddenimports += collect_submodules('win32con')

# Add specific imports
hiddenimports += [
    'pymsgbox',
    'pytweening',
    'pyscreeze',
    'mouseinfo',
    'pyperclip',
    'pyrect',
    'pygetwindow',
    'win32gui',
    'win32api',
    'win32con',
    'win32ui',
    'win32process',
    'win32com.client',
    '_ctypes',
    'pyautogui._pyautogui_win',
    'pyautogui._window_win'
]
```

## Step 3: Create Spec File

Create a file named `new_main.spec` in your project root with the following content:

```python
block_cipher = None

a = Analysis(
    ['src/main.py'],  # Update this path to your main script
    pathex=[],
    binaries=[],
    datas=[('src/instructions', 'instructions')],  # Update this with your data files
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
        'pymsgbox',
        'pytweening',
        'pyscreeze',
        'mouseinfo',
        'pyperclip',
        'pyrect'
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',  # This will be the name of your executable
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
```

## Step 4: Build the Executable

Run the following command to build the executable:

```powershell
.\.venv\Scripts\pyinstaller.exe new_main.spec --clean
```

The executable will be created in the `dist` directory.

## Important Notes

1. Update the following in the spec file for your project:
   - `src/main.py` path to match your main script
   - `datas` section to include your project's data files
   - `hiddenimports` to include any additional libraries your project uses

2. The executable should work on any Windows machine without requiring Python to be installed.

3. If you encounter missing module errors when running the executable, add the missing modules to the `hiddenimports` list in the spec file.

4. Make sure all required data files (images, config files, etc.) are properly included in the `datas` section of the spec file.

## Troubleshooting

If the executable fails to run:
1. Check the console output for missing module errors
2. Verify all dependencies are properly listed in `hiddenimports`
3. Ensure all required data files are included in `datas`
4. Try running with an older version of problematic dependencies (as we did with PyAutoGUI)
