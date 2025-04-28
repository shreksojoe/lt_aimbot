import psutil


process_name = "Label Traxx Client.exe"

def detect_label_traxx():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() in process_name.lower():
            return True
        return False

print(detect_label_traxx())

