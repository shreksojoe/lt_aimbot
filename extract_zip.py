import pyautogui
import pyperclip
import time
import re
from lt_click_tickets_button import button_coords, safe_moveTo, find_and_click_ui_element

def search_zip_code(address_zip):
    """
    Complete workflow for searching ZIP codes:
    1. Clicks Location link
    2. Scans ZIP column
    3. Handles popup window
    4. Returns True if match found
    """
    # Click Location link
    find_and_click_ui_element(
        key="location_link",
        prompt_text="Move your mouse over the Location link and press Enter to calibrate."
    )
    time.sleep(0.5)
    
    # Scan ZIP column
    found = scan_zip_column(address_zip)
    
    # Handle popup window
    handle_location_popup()
    
    return found

def scan_zip_column(address_zip):
    """Complete ZIP column scanning implementation"""
    if "address_top_row" not in button_coords:
        capture_top_row_coords()
    else:
        x = button_coords["address_top_row"]["x"]
        y = button_coords["address_top_row"]["y"]
    
    print(f"[INFO] Starting ZIP scan at ({x}, {y})")
    safe_moveTo(x, y, duration=0.5)
    time.sleep(0.5)
    
    # Initial click and copy
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    initial_content = sanitize_clipboard_text()
    
    # Scan logic
    row = 1
    previous_content = initial_content
    repeat_count = 0
    found = False
    
    while True:
        pyautogui.press('down')
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.3)
        current_content = sanitize_clipboard_text()
        
        # Repeat detection
        if current_content == previous_content:
            repeat_count += 1
            if repeat_count >= 2:
                break
        else:
            repeat_count = 0
            previous_content = current_content
            
        if address_zip in current_content:
            found = True
            break
            
        row += 1
    
    if found:
        print("[SUCCESS] Found matching ZIP code")
    else:
        print("[INFO] No matching ZIP code found")
    return found

def handle_location_popup():
    """Handle the location popup window"""
    find_and_click_ui_element(
        key="location_popup_ok",
        prompt_text="Move mouse to OK button in popup and press Enter"
    )
    time.sleep(0.5)

def sanitize_clipboard_text():
    """Clean clipboard text"""
    text = pyperclip.paste()
    if text:
        text = ''.join(c for c in text if c.isprintable() or c.isspace())
        return text.strip()
    return ""

def capture_top_row_coords():
    """Capture coordinates of top address row"""
    find_and_click_ui_element(
        key="address_top_row",
        prompt_text="Move mouse to top address row and press Enter"
    )
