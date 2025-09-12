import os
import sys

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller bundle.
    Always resolves relative to the install location, not the working directory.
    Updated: Always looks in the 'src' subfolder for resources, matching the install structure.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, 'src', relative_path)
