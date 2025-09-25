from datetime import datetime
import os
from pathlib import Path
import sys

# text: 

def standardize_date(date_str):
    if date_str is None:
        return ""

    # Ensure string, strip spaces
    date_str = str(date_str).strip()

    # Normalize ISO-like inputs (replace T with space, drop time if present)
    date_only = date_str.replace('T', ' ').split(' ')[0]

    separators = ['/', '-', '.', ' ']
    formats = []

    # Generate a broad set of formats for each separator
    for sep in separators:
        formats.extend([
            f"%m{sep}%d{sep}%Y",  # 12-31-2025
            f"%m{sep}%d{sep}%y",  # 12-31-25
            f"%d{sep}%m{sep}%Y",  # 31-12-2025
            f"%d{sep}%m{sep}%y",  # 31-12-25
            f"%Y{sep}%m{sep}%d",  # 2025-12-31
            f"%y{sep}%m{sep}%d",  # 25-12-31
        ])

    # Add explicit formats for ISO and common machine-generated dates
    formats.extend([
        "%Y-%m-%d",      # 2025-09-26
        "%Y/%m/%d",      # 2025/09/26
        "%m/%d/%Y",      # 09/26/2025
        "%d/%m/%Y",      # 26/09/2025
        "%m/%d/%y",      # 09/26/25
        "%d/%m/%y",      # 26/09/25
    ])

    # Try parsing against all formats
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_only, fmt)
            return parsed_date.strftime("%m/%d/%Y")
        except ValueError:
            continue

    # Fallback: return original input to avoid breaking pipelines
    return date_str

# files:

def _search_same_drive(filename: str, base_path: Path) -> Path | None:
    """Search for filename anywhere on the same drive as base_path.

    This is a last-resort search and can be slow. We prune common system
    directories to mitigate performance. Returns the first match found,
    or None if not found.
    """
    # Determine the drive root (e.g., 'C:\\')
    drive_root = Path(base_path.anchor)
    if not drive_root.exists():
        return None

    target_name = Path(filename).name.lower()
    # Common heavy/system dirs to skip to reduce traversal time
    prune_dirs = {
        'Windows', 'Program Files', 'Program Files (x86)', 'ProgramData',
        '$Recycle.Bin', 'System Volume Information', 'AppData', 'Microsoft OneDrive'
    }

    for root, dirs, files in os.walk(drive_root, topdown=True):
        # Prune directories in-place
        dirs[:] = [d for d in dirs if d not in prune_dirs]
        # Case-insensitive match on Windows
        for f in files:
            if f.lower() == target_name:
                return Path(root) / f
    return None

def find_abs_path(filename, extra_paths=None):
    """Return the absolute Path to filename if it exists, otherwise None.

    Resolution order:
    1) If filename is absolute and exists, return it.
    2) Current working directory.
    3) Same directory as this script (if __file__ is defined).
    4) Any optional paths provided via extra_paths.
    5) Common system install paths (Program Files, Program Files (x86) on Windows).
    6) Last resort: search the same drive.
    """
    p = Path(filename)

    # 1) Absolute path provided
    if p.is_absolute():
        return p.resolve() if p.exists() else None

    # 2) Current working directory
    candidate = Path.cwd() / filename
    if candidate.exists():
        return candidate.resolve()

    # 3) Same directory as this script
    if "__file__" in globals():
        script_dir = Path(__file__).parent
        candidate = script_dir / filename
        if candidate.exists():
            return candidate.resolve()

    # 4) Extra paths
    if extra_paths:
        for path in extra_paths:
            candidate = Path(path) / filename
            if candidate.exists():
                return candidate.resolve()

    # 5) Common system install paths (Windows only)
    if sys.platform.startswith("win"):
        program_files = [
            os.environ.get("ProgramFiles"),
            os.environ.get("ProgramFiles(x86)")
        ]
        for pf in program_files:
            if pf:  # env var exists
                candidate = Path(pf) / filename
                if candidate.exists():
                    return candidate.resolve()
                # Search one level deeper (Program Files\Subdir\filename)
                for subdir in Path(pf).iterdir():
                    if subdir.is_dir():
                        candidate = subdir / filename
                        if candidate.exists():
                            return candidate.resolve()

    # 6) Last resort: search the same drive
    try:
        base_for_drive = Path.cwd()
    except Exception:
        base_for_drive = Path(__file__).parent
    found = _search_same_drive(filename, base_for_drive)
    if found and found.exists():
        return found.resolve()

    return None

def find_rel_path(filename):
    """Return Path to filename relative to the caller's current working directory.

    If the file can be resolved via find_abs_path, we compute the relative
    path from Path.cwd(); otherwise, return None.
    """
    abs_path = find_abs_path(filename)
    if abs_path is None:
        return None
    try:
        return abs_path.relative_to(Path.cwd())
    except ValueError:
        # If abs_path is on a different drive or outside cwd's tree, use relpath
        return Path(os.path.relpath(abs_path, Path.cwd()))

    # cwd = Path.cwd()
    # for root, dirs, files in os.walk(cwd):
    #     if filename in files:
    #         abs_path = Path(root) / filename
    #         return abs_path.relative_to(cwd)
    # return None
