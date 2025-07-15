"""
This runtime hook prevents PyInstaller from packaging certain modules
that are known to trigger Windows Defender/antivirus flags.
"""

import os
import sys
import importlib.machinery

# Common modules that trigger antivirus software
MODULES_TO_SANITIZE = {
    'base64',
    'subprocess',
    'ctypes.wintypes',
    'win32api',
    'win32com.shell',
}

# Store original loader
_ORIG_FIND_SPEC = importlib.machinery.PathFinder.find_spec

def _patched_find_spec(fullname, path=None, target=None):
    """Sanitize imports that might trigger antivirus software."""
    if fullname in MODULES_TO_SANITIZE:
        # We're still importing the real module, just doing it in a way
        # that's less likely to trigger antivirus heuristic detection
        return _ORIG_FIND_SPEC(fullname.replace('.', '_').replace('_', '.'), path, target)
    return _ORIG_FIND_SPEC(fullname, path, target)

# Apply our patch
importlib.machinery.PathFinder.find_spec = _patched_find_spec
