import os
import sys

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller bundle.
    Always resolves relative to the install location, not the working directory.
    Updated: Always looks in the 'src' subfolder for resources, matching the install structure.
    """
    try:
        # When bundled with PyInstaller, use the extracted folder
        base_path = sys._MEIPASS
    except Exception:
        # When running from source, determine if we're already in 'src' directory
        base_path = os.path.abspath('.')
        # If we're already in the src directory, don't add 'src' again
        if os.path.basename(base_path) == 'src':
            return os.path.join(base_path, relative_path)
    return os.path.join(base_path, 'src', relative_path)
