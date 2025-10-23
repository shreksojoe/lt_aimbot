import keyboard
import pyautogui
import ctypes
from ctypes import wintypes
import time
import win32gui
from pynput import keyboard as pynput_keyboard, mouse as pynput_mouse

import window

# Disable PyAutoGUI failsafe globally to prevent pausing on smaller screens
pyautogui.FAILSAFE = False

# user32 = ctypes.windll.user32
user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.windll.kernel32
EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
SetForegroundWindow = user32.SetForegroundWindow
IsWindowVisible = user32.IsWindowVisible

# Simple global vertical offset (in client pixels) applied to final client-based target (set to 0 to disable)
OFFSET_Y_PX = 0

# Ensure the process is DPI-aware so that cursor positioning matches physical pixels
def _init_dpi_awareness():
    """Try to enable Per-Monitor V2 DPI awareness, then Per-Monitor (shcore), then System DPI aware.

    Returns a string describing the mode that was set.
    """
    # Try Per-Monitor V2 via user32.SetProcessDpiAwarenessContext
    try:
        DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = ctypes.c_void_p(-4)
        if hasattr(user32, 'SetProcessDpiAwarenessContext'):
            ok = user32.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
            if ok:
                print("[DPI] Set to Per-Monitor V2 via user32.SetProcessDpiAwarenessContext")
                return "per_monitor_v2"
    except Exception:
        pass

    # Try Per-Monitor via shcore.SetProcessDpiAwareness
    try:
        shcore = ctypes.windll.shcore
        PROCESS_PER_MONITOR_DPI_AWARE = 2
        hr = shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
        # 0 == S_OK, 0x5 == E_ACCESSDENIED (already set)
        if hr == 0 or hr == 0x5:
            print("[DPI] Set to Per-Monitor via shcore.SetProcessDpiAwareness")
            return "per_monitor"
    except Exception:
        pass

    # Fallback: System DPI aware
    try:
        user32.SetProcessDPIAware()
        print("[DPI] Set to System DPI aware via user32.SetProcessDPIAware")
        return "system"
    except Exception:
        print("[DPI] Failed to set DPI awareness; behavior may be off on scaling monitors")
        return "unknown"

_dpi_mode = _init_dpi_awareness()

def maneuver(process_name):
    """Highlights window, console, presses enter, and returns to window."""
    window.highlight_window(process_name)
    time.sleep(0.5)

    # highlight last window 
    window.highlight_console()
    time.sleep(0.5)

    # press enter on it
    pyautogui.press("enter")
    time.sleep(0.5)

    window.highlight_window(process_name)


def capture_mouse_relative(hwnd):
    """Capture mouse coordinates relative to window's upper-left corner.
    
    Args:
        hwnd (int): Window handle to capture coordinates relative to.
        
    Press Enter to capture coordinates, Escape to exit.
    """
    print("Move to the desired window. Press Enter when ready to capture coordinates.")
    print("Press Ctrl + c at any time to stop.")

    while True:
        # Wait for Enter to capture
        keyboard.wait('enter')  

        # Check if Escape was pressed before Enter
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            break

        if not hwnd:
            print("No active window detected. Try again.")
            continue

        # Get window position
        print("hwnd: ", hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)

        # Get current mouse position
        mouse_x, mouse_y = pyautogui.position()

        # Calculate coordinates relative to the window
        rel_x = mouse_x - left
        rel_y = mouse_y - top

        print(f"Captured coordinates relative to window: ({rel_x}, {rel_y})")

        # Small delay to avoid double captures if Enter is held down
        time.sleep(0.2)

        # Check if Escape is pressed to exit loop
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            break


def capture_mouse_absolute(hwnd):
    """Capture absolute screen coordinates of mouse position.
    
    Args:
        hwnd (int): Window handle (not used but kept for API consistency).
        
    Press Enter to capture coordinates, Escape to exit.
    """
    mouse_controller = pynput_mouse.Controller()

    def on_press(key):
        try:
            if key == pynput_keyboard.Key.enter:
                x, y = mouse_controller.position  # current screen position
                print(f"Captured screen=({x},{y})")
            elif key == pynput_keyboard.Key.esc:
                print("Exiting...")
                return False  # stop listener
        except Exception as e:
            print("Error:", e)

    with pynput_keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    return


def scale_to_current_monitor(x: int, y: int, reference_width: int = 1920, reference_height: int = 1080) -> tuple[int, int]:
    """Scale coordinates from reference resolution to current monitor resolution.
    
    Args:
        x (int): X coordinate from reference resolution.
        y (int): Y coordinate from reference resolution.
        reference_width (int): Reference width (default 1920).
        reference_height (int): Reference height (default 1080).
        
    Returns:
        tuple[int, int]: Scaled (x, y) coordinates for current monitor.
    """
    # Get current monitor resolution
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # Calculate scale factors
    scale_x = screen_width / reference_width
    scale_y = screen_height / reference_height

    # Apply scaling
    scaled_x = int(x * scale_x)
    scaled_y = int(y * scale_y)

    return scaled_x, scaled_y


def move_abs(x, y, process_name=""):
    """Move cursor to absolute screen coordinates and click."""
    print("move abs winapi called")
    # Move cursor using Windows API
    user32.SetCursorPos(int(x), int(y))
    print(f"cursor moved to ({x}, {y}) via Windows API")

    time.sleep(1)
    pyautogui.click()


def move_rel(hwnd, x, y):
    """Move cursor to coordinates relative to window's upper-left corner.
    
    Args:
        hwnd (int): Window handle.
        x (int): X coordinate relative to window's left edge.
        y (int): Y coordinate relative to window's top edge.
    """
    if hwnd == 0:
        raise RuntimeError("No active window found")

    # Get window rectangle: (left, top, right, bottom)
    rect = ctypes.wintypes.RECT()
    print("hwnd: ", hwnd)
    user32.GetWindowRect(hwnd, ctypes.byref(rect))

    # Convert relative coordinates to absolute screen coordinates
    abs_x = rect.left + x
    abs_y = rect.top + y

    # Move the mouse
    pyautogui.FAILSAFE = False
    user32.SetCursorPos(abs_x, abs_y)
    print("move possition")
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)

def select_all():
    for _ in range(12):
        keyboard.send('backspace')
    time.sleep(1)

def compare_text(text):
    # copy
    pyautogui.hotkey('ctrl','c')
    clipboard_text = pyperclip.paste()

    if text == clipboard_text:
        return True
    else:
        return False










