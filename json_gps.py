import json
import pygetwindow as gw
import pyautogui
import subprocess
import time
import sys
import csv

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
    zip_code = 0
    for coord in instructions:
        if isinstance(coord, list) and len(coord) == 2 and all(isinstance(x, (int, float)) for x in coord):
            pyautogui.moveTo(coord[0], coord[1], duration=0.2)
            pyautogui.click()
            time.sleep(1)
        elif isinstance(coord, int):
            print(f"Coord is {type(coord)}")
            zip_code = coord
        else:
            pyautogui.write(coord)
            time.sleep(1)

    return zip_code

if len(sys.argv) > 2:
    arg_json = sys.argv[1]
    info = read_json(arg_json)
    true_zip_code = read_coords(info)

subprocess.run(['pythonw.exe', 'address_search.py', str(true_zip_code)])
    

# goes from process_csv

# goes to address_search
