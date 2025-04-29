import psutil
import pygetwindow as gw
import win32gui
import win32process
import win32con


# detect if label traxx is running
def detect_label_traxx(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            return True
    return False


# get lt window from pid
def get_pid_from_process_name(process_name):
    for proc in psutil.process_iter(['name' , 'pid']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            return proc.info['pid']
    return None
    

# get window handle for labeltraxx (so we can get the title)
def get_hwnd_from_pid(pid):

    # verify that the window has a handle
    for window in gw.getAllWindows():
        try:
            if window._getWindowHandle() and window._hWnd:
                pass
        except Exception:
            continue

    for window in gw.getAllWindows():
        hwnd = window._hWnd
        _, win_pid = win32process.GetWindowThreadProcessId(hwnd)
        if win_pid == pid:
            return window.title

    return None


# bring lt to the front
def select_label_traxx(lt_title):

    windows = gw.getWindowsWithTitle(lt_title)
    lt_instance = detect_label_traxx(lt_title)
        
    if lt_instance:
        for window in gw.getAllWindows():
            if window.title and title.lower() in window.title.lower():
                if window.isMinimized:
                    window.restore
                window.activate
    else:
        print("Label Traxx is not open")
    

label_traxx = "Label Traxx Client.exe"
lt_pid = get_pid_from_process_name(label_traxx)
lt_hwnd = get_hwnd_from_pid(lt_pid)
print(lt_hwnd)

