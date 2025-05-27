from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "pyautogui", "keyboard", "pygetwindow", "json", "csv", "sys"],
    "include_files": ["instructions/"],  # Include your JSON files
    "excludes": []
}

setup(
    name="lt_aimbot",
    version="1.0",
    description="Label Traxx Automation Tool",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/main.py", base=None)]
)
