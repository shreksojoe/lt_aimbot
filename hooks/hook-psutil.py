"""
PyInstaller hook for psutil.

This hook ensures that all necessary modules and binaries for psutil are included in the final executable.
"""
from PyInstaller.utils.hooks import collect_all

# Collect all psutil modules and binaries
datas, binaries, hiddenimports = collect_all('psutil')

# Ensure these are included in the bundle
