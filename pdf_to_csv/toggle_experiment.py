import win32gui
import win32con
import win32process
import subprocess
import time

lt_process_name = "Label Traxx Client.exe"
lt_path = r"C:\\Program Files\\LT Client\\Label Traxx Client.exe"

def wait_on_program(process_name):
    timeout=30
    pid = get_pid(process_name)
    start_time = time.time()
    while time.time() - start_time < timeout:
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == '':
            return
        else:
            pass
        time.sleep(0.5)
    print("Program timed out")

def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

# Launch two Notepad windows
p1 = subprocess.Popen([lt_path])
p2 = subprocess.Popen([lt_path])

wait_on_program(lt_process_name)
# Get their window handles by PID
print(get_hwnds_for_pid(p1.pid)[0])
hwnd1 = get_hwnds_for_pid(p1.pid)[0]
hwnd2 = get_hwnds_for_pid(p2.pid)[0]

# Toggle between them
win32gui.ShowWindow(hwnd1, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd1)
time.sleep(2)

win32gui.ShowWindow(hwnd2, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd2)
