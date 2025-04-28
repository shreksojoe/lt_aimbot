import psutil


#program_name = "Label Traxx Client.exe"

def detect_label_traxx(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            return True
    return False

print(detect_label_traxx("Label Traxx Client.exe"))



