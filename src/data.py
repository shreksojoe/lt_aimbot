import re
import json
from datetime import datetime, timedelta
import os
from pathlib import Path
import sys
import motion
import window
import pyperclip
import pyautogui
import time
import keyboard
import usaddress

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

def move_to_wed(date_str):
    date = datetime.strptime(date_str, "%m/%d/%Y")
    # weekday(): Monday=0, Tuesday=1, ..., Sunday=6
    days_ahead = (2 - date.weekday()) % 7  # Wednesday is 2
    next_wed = date + timedelta(days=days_ahead)
    return next_wed.strftime("%m/%d/%Y")

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

def find_rel_path(filename, max_depth=5):
    """
    Search for the closest file named `filename` relative to CWD.
    Expands outward: current dir → children → parent → deeper children → higher parents...
    Returns the relative path or None if not found.
    """
    cwd = Path.cwd()
    
    # Step 1: check current directory directly
    candidate = cwd / filename
    if candidate.exists():
        return Path(filename)  # relative already

    # Expand outward
    for depth in range(1, max_depth + 1):
        # --- search downward (subdirectories) ---
        for path in cwd.rglob(filename):
            # limit depth by relative part length
            if len(path.relative_to(cwd).parts) <= depth + 1:
                try:
                    return path.relative_to(cwd)
                except ValueError:
                    return Path(os.path.relpath(path, cwd))

        # --- search upward (parent directories) ---
        if cwd.parents and depth <= len(cwd.parents):
            parent = cwd.parents[depth - 1]
            candidate = parent / filename
            if candidate.exists():
                try:
                    return candidate.relative_to(cwd)
                except ValueError:
                    return Path(os.path.relpath(candidate, cwd))

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

def address_search(text):
    pyperclip.copy("")
    process_name = "Label Traxx Client.exe"
    window.highlight_window(process_name)
    hwnd = window.get_hwnd(process_name)
    print("Testing title")
    
    # Check title without blocking - use title_contains_option instead
    current_title = window.get_title()
    print(f"Current window title: {current_title}")
    
    if ("Editing Ticket" in current_title) or ("Editing Stock Ticket" in current_title):
        motion.move_rel(hwnd, 157, 284)
        # time.sleep(0.4)
        print("ran through the right title")
    else: 
        print(f"Wrong title: '{current_title}' - continuing anyway...")
    hwnd = window.get_hwnd(process_name)
    repeat = 0
    x = 176
    y = 122
    motion.move_rel(hwnd, x, y)
    rep = 10
    reach_end = 0
    print("got to the for loop")
    for _ in range(35):
        past_address = pyperclip.paste()
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.4)
        current_address = pyperclip.paste()
        print("searching... ", current_address)
        if text.lower() in current_address.lower():
            pyautogui.click()
            motion.move_rel(hwnd, 780, 346)
            # pyautogui.press("enter")
            return True
        elif current_address == past_address:
            print("curr: ", current_address, "past: ", past_address)
            repeat += 1
            if repeat <= 3:
                return False
        elif reach_end >= 9:
            print("end of 9")
            pyautogui.press("down")
            pyautogui.click()
        elif reach_end < 9:
            reach_end += 1
            print("still moving down: ", reach_end)
            y += 19
            motion.move_rel(hwnd, x, y)
            # pyautogui.click()
    motion.move_rel(hwnd, 781, 343)

def compare(expected: str):

    # Simulate Ctrl+C
    time.sleep(2) 
    pyperclip.copy("")
    pyautogui.hotkey("ctrl", "c")
    # Small delay to let clipboard update
    pyautogui.sleep(0.1)
    
    # Get clipboard text
    clipboard_text = pyperclip.paste()
    
    # Compare with expected string
    if clipboard_text != expected:
        print(f"[ERROR] Clipboard text does not match expected.")
        print(f"  Expected: {expected!r}")
        print(f"  Got:      {clipboard_text!r}")
        input("Press Enter to resume...")

def write(text):
    time.sleep(1)
    print("typing: ", text)
    keyboard.write(text)
    time.sleep(3)

def split_addr(address):
    # address = "ROLL PRODUCTS INC. THE OAKWOOD GROUP26504-OMF-ME-NMORHAN9755 INKSTER RDTAYLOR, MI 48180US"

    # Remove leading company if present
    address = re.sub(r'^ROLL PRODUCTS INC\. ?', '', address, flags=re.IGNORECASE)

    # Extract country (assume US)
    country = "US" if address.endswith("US") else ""
    address = re.sub(r'US$', '', address)

    # Extract state and zip at the end (more specific pattern)
    state_zip_match = re.search(r',\s*([A-Z]{2})\s*(\d{5})$', address)
    if state_zip_match:
        state, zip_code = state_zip_match.groups()
        # Remove the state and zip from address
        address = address[:state_zip_match.start()].strip()
    else:
        state = zip_code = ""

    # Now find the street address with suffix (RD, ST, etc.)
    # This should come before the city
    street_match = re.search(r'(\d{1,5}[-A-Z]*\d*\s+[A-Z\s]+?(?:RD|ST|AVE|BLVD|LN|CT))\s*([A-Z]+)$', address)
    
    if street_match:
        line2 = street_match.group(1).strip()
        city = street_match.group(2).strip()
        line1 = address[:street_match.start()].strip()
    else:
        # Fallback: try to extract city as last word
        city_match = re.search(r'([A-Z]+)$', address)
        if city_match:
            city = city_match.group(1)
            main_address = address[:city_match.start()].strip()
            
            # Try to find street address in remaining text
            street_match2 = re.search(r'(\d{1,5}[-A-Z]*\d*\s+[A-Z\s]+?(?:RD|ST|AVE|BLVD|LN|CT))\s*$', main_address)
            if street_match2:
                line2 = street_match2.group(1).strip()
                line1 = main_address[:street_match2.start()].strip()
            else:
                line1 = main_address
                line2 = ""
        else:
            city = ""
            line1 = address
            line2 = ""

    return [line1, line2, city, state, zip_code, country]

def swap_slash(path):
    return path.replace("/", "\\")

def load_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
