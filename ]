import psutil
import pygetwindow as gw
import win32gui
import win32process
import win32con
import subprocess
import time
import json
import pyautogui


# detect if label traxx is running
def detect_process(process_name):
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
def get_hwnd_or_title_from_pid(pid, output):

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
            if output.lower() == "title":
                return window.title
            elif output.lower() == "handle":
                return window._hWnd
            else:
                print(f"{output} wasn't an option. Please pick handle or title")

    return None


# bring lt to the front
def select_program(window_handle):

    win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(window_handle)

# start a program
def start_program(program_path): subprocess.Popen([program_path])

# wait for program 
def wait_for_program(pid, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == '':
            print("Program is opened")
            return
        else:
            exit
        time.sleep(0.5)
    print("Program Timed Out")

# read json and return value
def read_json(file_name):
    with open (file_name, 'r') as file:
        data = json.load(file)
        value_list = []
        for element in data:
            # exception "Name"
            for key, value in element.items():
                if key != "Name":
                    value_list.append(value)
        return value_list

def read_coords(instructions):
    for coord in instructions:
        # pyautogui.click(x=coord[0], y=coord[1]) 
        if isinstance(coord, list) and len(coord) == 2 and all(isinstance(x, (int, float)) for x in coord):
            pyautogui.moveTo(coord[0], coord[1], duration=0.2)
            pyautogui.click()
            time.sleep(0.2)
        else:
            pyautogui.write(coord)
            time.sleep(0.2)

# variables
lt_process_name = "Label Traxx Client.exe"
lt_path = r"C:\\Program Files\\LT Client\\Label Traxx Client.exe"
lt_pid = get_pid_from_process_name(lt_process_name)
lt_hwnd = get_hwnd_or_title_from_pid(lt_pid, "handle")
lt_title = get_hwnd_or_title_from_pid(lt_pid, "title")
login_info = read_json(r'C:\\Users\\Joseph.Stadum\\lt_aimbot\\login_credentials.json')
home_btn_info = read_json(r'C:\\Users\\Joseph.Stadum\\lt_aimbot\\home_btn.json')


# logic
if detect_process(lt_process_name):
    select_program(lt_hwnd)

    if "Home Page" in lt_title:
        print("Our work here is done")
    elif lt_title == '':
        read_coords(login_info)
    else:
        read_coords(home_btn_info)
        
else:
    start_program(lt_path)
    wait_for_program(lt_pid)
    read_coords(login_info)
    # log into program















