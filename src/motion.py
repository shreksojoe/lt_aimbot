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

def menuever(process_name):
    window.highlight_window(process_name)
    time.sleep(0.5)

    # highlight last window 
    window.highlight_console()
    time.sleep(0.5)

    # press enter on it
    pyautogui.press("enter")
    time.sleep(0.5)

    window.highlight_window(process_name)

# Example usage:
# Suppose your reference window is 800x600 and you want to move to (400,300) relative to that
def capture_mouse_relative(hwnd):
    print("Move to the desired window. Press Enter when ready to capture coordinates.")
    print("Press Ctrl + c at any time to stop.")

    while True:
        # Wait for Enter to capture
        keyboard.wait('enter')  

        # Check if Escape was pressed before Enter
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            break

        # hwnd = window.get_hwnd("") 
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

def move_abs(x, y, process_name, retries=2):
#     pyautogui.FAILSAFE = False  # Disable failsafe to prevent pausing on smaller screens
#     pyautogui.moveTo(x, y)
#     pyautogui.click()
#     time.sleep(0.4)
    
    for attempt in range(retries):

        """Alternative cursor movement using direct Windows API calls"""
        print("move abs winapi called")
        
        # Move cursor using Windows API
        success = user32.SetCursorPos(int(x), int(y))
        if success:
            print(f"cursor moved to ({x}, {y}) via Windows API")
        else:
            print(f"failed to move cursor to ({x}, {y})")
            return
        
        # Small delay to ensure cursor is positioned
        time.sleep(0.1)
        
        # Click using Windows API
        # Get current cursor position to ensure we're clicking at the right spot
        cursor_pos = ctypes.wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(cursor_pos))
        print(f"clicking at ({cursor_pos.x}, {cursor_pos.y})")

        # because damn pause
        pyautogui.press("enter")
        window.highlight_window(process_name)
        
        # Send mouse down and up events
        user32.mouse_event(0x0002, cursor_pos.x, cursor_pos.y, 0, 0)  # MOUSEEVENTF_LEFTDOWN
        time.sleep(0.05)
        user32.mouse_event(0x0004, cursor_pos.x, cursor_pos.y, 0, 0)  # MOUSEEVENTF_LEFTUP
        
        print("click completed via Windows API")
        time.sleep(0.4)

def move_rel(hwnd, x, y):

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

def adjust_to_screen(process_name, rel_x, rel_y):
    hwnd = win32gui.GetForegroundWindow()

    # Get window rectangle (left, top, right, bottom)
    print("hwnd: ", hwnd)
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect

    # Absolute coordinates = window top-left + relative offset
    abs_x = left + rel_x
    abs_y = top + rel_y

    return abs_x, abs_y

def coords_to_ratio(hwnd, x, y):
    """
    Convert absolute pixel coordinates inside a window's client area
    to normalized ratios (0.0 - 1.0).
    
    Args:
        hwnd (int): Window handle.
        x (int): X coordinate inside client area.
        y (int): Y coordinate inside client area.
    
    Returns:
        (float, float): (x_ratio, y_ratio)
    """
    rect = ctypes.wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top

    if width <= 0 or height <= 0:
        raise RuntimeError("Window has invalid dimensions")

    x_ratio = x / width
    y_ratio = y / height
    return x_ratio, y_ratio

def move_rel_normalized(hwnd, x_ratio, y_ratio):
    """
    Move mouse to position relative to the client area of a window.

    Args:
        hwnd (int): Window handle.
        x_ratio (float): X position as fraction of window width (0.0 - 1.0).
        y_ratio (float): Y position as fraction of window height (0.0 - 1.0).
    """
    # x_ratio, y_ratio = coords_to_ratio(hwnd, x, y)
    print("x ratio: ", x_ratio)
    print("y ratio: ", y_ratio)

    if hwnd == 0:
        raise RuntimeError("No active window found")

    # Get client rect (relative to window client area)
    rect = ctypes.wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))

    width = rect.right - rect.left
    height = rect.bottom - rect.top

    if width <= 0 or height <= 0:
        raise RuntimeError("Window has invalid dimensions")

    # Clamp ratios to [0, 1] to avoid out-of-bounds
    x_ratio = max(0.0, min(1.0, x_ratio))
    y_ratio = max(0.0, min(1.0, y_ratio))

    # Convert normalized coords to client coords
    client_x = int(width * x_ratio)
    client_y = int(height * y_ratio)

    # Apply simple vertical offset and clamp within client bounds (client-based moves only)
    if OFFSET_Y_PX:
        client_y_before = client_y
        client_y = max(0, min(height - 1, client_y + OFFSET_Y_PX))
        print(f"Applied OFFSET_Y_PX={OFFSET_Y_PX}: client_y {client_y_before} -> {client_y} (height={height})")

    # For diagnostics: where is the client origin in screen space?
    client_origin = ctypes.wintypes.POINT(0, 0)
    user32.ClientToScreen(hwnd, ctypes.byref(client_origin))
    print(f"Client origin (screen): ({client_origin.x}, {client_origin.y}) | client size: {width}x{height}")

    # Convert client coords to screen coords
    point = ctypes.wintypes.POINT(client_x, client_y)
    user32.ClientToScreen(hwnd, ctypes.byref(point))
    print(f"Client target -> screen: client=({client_x},{client_y}) -> screen=({point.x},{point.y})")

    # Bring target window to foreground to ensure consistent z-order and focus
    try:
        SetForegroundWindow(hwnd)
        time.sleep(0.05)
    except Exception:
        pass

    # Move mouse with diagnostics
    ok = user32.SetCursorPos(point.x, point.y)
    if not ok:
        err = ctypes.get_last_error()
        print(f"[cursor] SetCursorPos failed (normalized): ({point.x},{point.y}) | error={err}")
    else:
        print(f"[cursor] SetCursorPos OK (normalized): ({point.x},{point.y})")
    time.sleep(0.5)
    # pyautogui.moveTo(point.x, point.y)
    print(f"Moved to {point.x}, {point.y} (monitor aware)")

def move_rel_pixels(hwnd, x, y):
    rect = ctypes.wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    pt = ctypes.wintypes.POINT(x, y)
    user32.ClientToScreen(hwnd, ctypes.byref(pt))
    user32.SetCursorPos(pt.x, pt.y)
    print(f"Moved to {pt.x}, {pt.y} (monitor aware)")

def coords_from_screen_to_ratio(hwnd, screen_x, screen_y):
    """Convert screen coordinates to ratios relative to a window's client area."""
    rect = ctypes.wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top

    if width <= 0 or height <= 0:
        raise RuntimeError("Invalid window dimensions")

    # For diagnostics: where is the client origin in screen space?
    client_origin = ctypes.wintypes.POINT(0, 0)
    user32.ClientToScreen(hwnd, ctypes.byref(client_origin))
    print(f"[normalize] Client origin (screen): ({client_origin.x}, {client_origin.y}) | client size: {width}x{height}")

    # Convert screen point to client coordinates
    pt = ctypes.wintypes.POINT(screen_x, screen_y)
    user32.ScreenToClient(hwnd, ctypes.byref(pt))
    print(f"[normalize] Screen -> client: screen=({screen_x},{screen_y}) -> client=({pt.x},{pt.y})")

    # Normalize
    x_ratio = pt.x / width
    y_ratio = pt.y / height
    print(f"[normalize] Ratios: ({x_ratio:.4f}, {y_ratio:.4f})")
    return x_ratio, y_ratio


def collect_coords(hwnd):
    """
    Collect coordinates when ENTER is pressed.
    Exit when ESCAPE is pressed.
    """
    results = []
    mouse_controller = pynput_mouse.Controller()

    def on_press(key):
        nonlocal results
        try:
            if key == pynput_keyboard.Key.enter:
                x, y = mouse_controller.position  # current screen position
                x_ratio, y_ratio = coords_from_screen_to_ratio(hwnd, x, y)
                print(f"Captured screen=({x},{y}) → ratios=({x_ratio:.4f}, {y_ratio:.4f})")
                results.append(((x, y), (x_ratio, y_ratio)))
            elif key == pynput_keyboard.Key.esc:
                print("Exiting...")
                return False  # stop listener
        except Exception as e:
            print("Error:", e)

    with pynput_keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    return results


# ------------------------------
# Reusable helpers (exportable)
# ------------------------------

def get_client_size(hwnd):
    """Return (width, height) of the client area for hwnd."""
    rect = ctypes.wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    return (rect.right - rect.left, rect.bottom - rect.top)


def get_window_rect(hwnd):
    """Return (left, top, right, bottom) of the outer window (including title bar/borders)."""
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom


def get_client_origin_in_screen(hwnd):
    """Return (x, y) of the client area's top-left in screen coordinates."""
    pt = ctypes.wintypes.POINT(0, 0)
    user32.ClientToScreen(hwnd, ctypes.byref(pt))
    return pt.x, pt.y


def wait_for_window_title_contains(title_substring, timeout_seconds=30.0, poll_seconds=0.5):
    """Wait for the foreground window title to contain the given substring. Return hwnd or None on timeout."""
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        if title_substring in title:
            return hwnd
        time.sleep(poll_seconds)
    return None


def select_window_by_title(title_substring, timeout_seconds=30.0, focus_delay=0.25):
    """Block until the foreground window title contains substring and return hwnd. Adds a small delay for stability."""
    hwnd = wait_for_window_title_contains(title_substring, timeout_seconds)
    if hwnd:
        # Small delay to allow dialogs to finish layout
        time.sleep(focus_delay)
    return hwnd


def set_current_window_by_title(title_substring, timeout_seconds=30.0):
    """Wait for a window whose title contains substring and return its hwnd. Prints helpful logs."""
    print("Waiting for window containing:", title_substring)
    hwnd = select_window_by_title(title_substring, timeout_seconds)
    if not hwnd:
        raise TimeoutError(f"Timed out waiting for window containing: {title_substring}")
    print("Focused window:", win32gui.GetWindowText(hwnd))
    return hwnd


def coords_to_ratios_general(hwnd, x, y, input_mode: str = "auto"):
    """
    Convert arbitrary input coordinates (which may be ratios [0..1], screen pixels, or client pixels)
    into normalized ratios relative to hwnd's client area.

    input_mode: 'auto' | 'ratio' | 'screen' | 'client' | 'window'
      - 'window' means pixels relative to the outer window's top-left (title bar included)

    Returns: (rat_x, rat_y), mode used -> one of "ratio", "screen", "client", "window".
    """
    width, height = get_client_size(hwnd)
    if width <= 0 or height <= 0:
        raise RuntimeError("Invalid client size while converting coordinates")

    # Precompute window/client offsets for 'window' mode
    win_l, win_t, win_r, win_b = get_window_rect(hwnd)
    client_sx, client_sy = get_client_origin_in_screen(hwnd)
    vertical_chrome = client_sy - win_t  # title bar + menu height
    horizontal_chrome = client_sx - win_l  # left border width

    # Explicit modes
    if input_mode == "ratio":
        return (float(x), float(y)), "ratio"
    if input_mode == "client":
        return (x / width, y / height), "client"
    if input_mode == "screen":
        rx, ry = coords_from_screen_to_ratio(hwnd, x, y)
        return (rx, ry), "screen"
    if input_mode == "window":
        # Convert window-relative pixels → client pixels by removing window chrome offsets
        cx = (x - horizontal_chrome)
        cy = (y - vertical_chrome)
        print(f"[window->client] chrome offsets: dx={horizontal_chrome}, dy={vertical_chrome}; window ({x},{y}) -> client ({cx},{cy})")
        return (cx / width, cy / height), "window"

    # Auto mode
    # Case 1: Already normalized ratios
    if isinstance(x, float) and isinstance(y, float) and 0.0 <= x <= 1.0 and 0.0 <= y <= 1.0:
        return (x, y), "ratio"

    # Case 2: If integers within current client bounds, treat as client-relative pixels first
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        if 0 <= x <= width and 0 <= y <= height:
            rat_client_x = x / width
            rat_client_y = y / height
            return (rat_client_x, rat_client_y), "client"

    # Case 3: Try interpreting as screen coordinates
    rat_x, rat_y = coords_from_screen_to_ratio(hwnd, x, y)
    if 0.0 <= rat_x <= 1.0 and 0.0 <= rat_y <= 1.0:
        return (rat_x, rat_y), "screen"

    # Fallback: attempt window-relative pixels
    cx = (x - horizontal_chrome)
    cy = (y - vertical_chrome)
    return (cx / width, cy / height), "window"

    raise RuntimeError("Invalid client size while converting coordinates")


def move_window_pixels(hwnd, x, y):
    """Move to window-absolute pixels (non-client allowed): target = (window_left + x, window_top + y)."""
    l, t, r, b = get_window_rect(hwnd)
    sx = int(l + x)
    sy = int(t + y)
    print(f"[move_window_pixels] window rect=({l},{t},{r},{b}) | target screen=({sx},{sy})")
    ok = user32.SetCursorPos(sx, sy)
    if not ok:
        err = ctypes.get_last_error()
        print(f"[cursor] SetCursorPos failed (window_abs): ({sx},{sy}) | error={err}")
    else:
        print(f"[cursor] SetCursorPos OK (window_abs): ({sx},{sy})")


def move_screen_pixels(hwnd, screen_x, screen_y):
    """Move to absolute screen pixels (ignores hwnd except for consistency of API)."""
    print(f"[move_screen_pixels] target screen=({screen_x},{screen_y})")
    ok = user32.SetCursorPos(int(screen_x), int(screen_y))
    if not ok:
        err = ctypes.get_last_error()
        print(f"[cursor] SetCursorPos failed (screen_abs): ({int(screen_x)},{int(screen_y)}) | error={err}")
    else:
        print(f"[cursor] SetCursorPos OK (screen_abs): ({int(screen_x)},{int(screen_y)})")


def move_to_input_coords(hwnd, x, y, input_mode: str = "auto"):
    """Interpret (x,y) and move accordingly.

    input_mode: 'auto' | 'ratio' | 'screen' | 'client' | 'window' | 'window_abs' | 'screen_abs'
    """
    if input_mode == "window_abs":
        return move_window_pixels(hwnd, x, y)
    if input_mode == "screen_abs":
        return move_screen_pixels(hwnd, x, y)

    (rx, ry), mode = coords_to_ratios_general(hwnd, x, y, input_mode=input_mode)
    print(f"[coords] Using {mode} interpretation -> ratios=({rx:.4f}, {ry:.4f})")
    move_rel_normalized(hwnd, rx, ry)
