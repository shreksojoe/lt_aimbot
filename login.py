import psutil
import pygetwindow as gw

label_traxx = "Label Traxx Client.exe"


# detect if label traxx is running
def detect_label_traxx(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            return True
    return False

# get lt window from pid
def get_window_title_from_process_name(process_name):
    for proc in psutil.process_iter(['name' , 'pid']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            pid = proc.info['pid']

            for window in gw.getAllWindows():
                if window._hWnd:
                    try:
                        if window._getWindowPid() == pid:
                            return window.title
                    except Exception:
                        continue
                else:
                    return "No Title"
    

# bring lt to the front
def select_label_traxx(title):

    windows = gw.getWindowsWithTitle(label_traxx)
    lt_instance = detect_label_traxx(label_traxx)
        
    if lt_instance:
        for window in gw.getAllWindows():
            if window.title and title.lower() in window.title.lower():
                if window.isMinimized:
                    window.restore
                window.activate
                
    else:
        print("Label Traxx is not open")
    


select_label_traxx(" ")


print(get_window_title_from_process_name(label_traxx))
