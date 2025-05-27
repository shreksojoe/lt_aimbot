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
