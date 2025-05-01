import json
import pygetwindow as gw
import pyautogui
import time
import sys

# read json and return list
def read_json(file_name):
    with open (file_name, 'r') as file:
        data = json.load(file)
        value_list = []
        for element in data:
            #exception "Name"
            for key, value in element. items():
                if key != "Name":
                    value_list.append(value)

        return value_list

def read_coords(instructions):
    for coord in instructions:
        if isinstance(coord, list) and len(coord) == 2 and all(isinstance(x, (int, float)) for x in coord):
            active_window = gw.getWindowWithTitle(gw.getActiveWindow().title)[0]
            left, top = active_window.left, active_window.top
            x = left + coord[0] 
            y = top + coord[1]
            pyautogui.moveTo(x, y, duration=0.2)
            pyautogui.click()
            time.sleep(1)
        else:
            pyautogui.write(coord)
            time.sleep(1)


#if __name__ == "__main__":
#    home_btn_info = read_json(r'C:\\Users\Joseph.Stadum\\lt_aimbot\\ticket.json')
#    read_coords(home_btn_info)


if len(sys.argv) > 1:
    arg = sys.argv[1]
    info = read_json(arg)
    read_coords(info)

