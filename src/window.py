import psutil
import win32gui
import win32process
import win32con
import time
import pygetwindow as gw
import subprocess
import winreg
import os
import ctypes
import win32gui

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# informational:
# get pid
def get_pid(process_name):
    for proc in psutil.process_iter(['name' , 'pid']):
        if (proc.info['name'] and proc.info['name'].lower() == process_name.lower()):
            return(proc.info['pid'])
    return False

# get window handle
def get_titles(process_name):
    # get the pid
    pid = get_pid(process_name)

    if pid == False:
        return "process is not running"

    titles = []

    def callback(hwnd, _):
        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
        if window_pid == pid and win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                titles.append(title)
            elif not title:
                titles.append("")

    win32gui.EnumWindows(callback, None)
    if len(titles) > 1:
        return titles
    else:
        return titles

def get_all_window_titles():
    """Return a list of all window titles currently open."""
    titles = []

    def enum_windows_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:  # Skip empty titles
                titles.append(title)
    win32gui.EnumWindows(enum_windows_callback, None)
    return titles

# works but practically useless when it comes to Label traxx (way to many "hwnds")
# take in the title
def get_hwnds_from_pid(process_name):
    pid = get_pid(process_name)

    hwnds = []
    def callback(hwnd, hwnds):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            hwnds.append(hwnd)
        return True

    win32gui.EnumWindows(callback, hwnds)
    return hwnds

def get_title():
    # titles = get_titles(process_name)

    cw = user32.GetForegroundWindow()
    length = 512
    buffer = ctypes.create_unicode_buffer(512)
    user32.GetWindowTextW(cw, buffer, length)

    return buffer.value

# get the hwnd from the title
def get_hwnd(process_name):
    """Return a representative top-level hwnd for the given process name.

    Prefers a visible top-level window belonging to the process PID.
    Returns None if not found.
    """
    highlight_window(process_name)

    pid = get_pid(process_name)
    if not pid:
        return None

    target_hwnd = None

    def callback(hwnd, _):
        nonlocal target_hwnd
        try:
            if not win32gui.IsWindowVisible(hwnd):
                return True
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                # Take the first visible top-level window
                target_hwnd = hwnd
                return False  # stop enumeration
        except Exception:
            # Skip windows that can't be queried
            pass
        return True

    try:
        win32gui.EnumWindows(callback, None)
    except Exception:
        # If enumeration fails, return None
        pass
    return target_hwnd

# functional
def wait_on_program(process_name):
    timeout=30
    pid = get_pid(process_name)
    start_time = time.time()
    while time.time() - start_time < timeout:
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == '':
            return
        
    print("Program timed out")

# takes in process path
def launch_program(process_path):
    subprocess.Popen([process_path])
    process_name = os.path.basename(process_path)
    wait_on_program(process_name)

# return a boolean (is a process running yes or no)
def detect_process(process_name):
    for proc in psutil.process_iter(['name']):
        if (proc.info['name'] and
                proc.info['name'].lower() == process_name.lower()):
            return True
    return False

# input handle
def highlight_window(process_name):
    
    if not detect_process(process_name):
        print("Process is not running, no window to highlight")
        return False
    pid = get_pid(process_name)
    for window in gw.getAllWindows():
        try:
            if window._getWindowHandle() and window.hWnd:
                pass
        except Exception:
            continue
    for window in gw.getAllWindows():
        hwnd = window._hWnd
        _, win_pid = win32process.GetWindowThreadProcessId(hwnd)
        if win_pid == pid:
             handle = window._hWnd
    try:
        win32gui.ShowWindow(handle, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(handle)
    except UnboundLocalError:
        print("Window cannot be toggled (your likely in the login stage)")
        return False

# only works, if the titles are different
def toggle_window(process_name, iterations=1):
    cw_title = get_title()
    titles = get_titles(process_name)

    cw_index = 0
    if cw_title in titles:
        cw_index = titles.index(cw_title)
        print("current windows index: ", cw_index)
    try: 
        hwnd = user32.FindWindowW(None, titles[iterations])
        user32.ShowWindow(hwnd, 5)
        user32.SetForegroundWindow(hwnd)
    except IndexError:
        print("Not enough windows to toggle")
        return False
    except UnboundLocalError:
        print("Window cannot be toggled (your likely in the login stage)")
        return False

def highlight_by_title(text):
    # Find the window by title
    
    titles = get_all_window_titles()
    for title in titles:
        if text.lower() in title.lower():  # case-insensitive match
            hwnd = win32gui.FindWindow(None, title)
            if hwnd:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                print(f"Highlighted window: {title}")
                return
    print(f"No window found containing: {text}")

def title_contains(text, process_name=""):
    if process_name:
        highlight_by_title(text)
#        highlight_window(process_name)
        time.sleep(0.1)

    window_title = get_title()
    if text in window_title:
        return True
    else:
        while text not in get_title():
            time.sleep(5)

def title_contains_option(text, process_name=""):
    highlight_by_title(text)
    if process_name:
        # highlight_window(process_name)
        time.sleep(0.1)

    window_title = get_title()
    if text in window_title:
        return True
    else:
        time.sleep
        return False

def title_is_empty(process_name):
    highlight_window(process_name)
    window_title = get_title().replace(" ", "")
    if not window_title:
        print(window_title)
        return True
    else:
        print(window_title)
        return False
# we want to get the hwnd

def highlight_console(hwnd=None):
    if hwnd is None:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()

    # Restore window if minimized
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        # fallback if OS refuses focus
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


def get_title_hwnd(hwnd):
    title = win32gui.GetWindowText(hwnd)
    print(title)
    return title

def mark_hwnd():
    hwnd = win32gui.GetForegroundWindow()
    print(hwnd)
    return hwnd
