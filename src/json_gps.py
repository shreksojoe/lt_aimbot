import json
import keyboard
import pygetwindow as gw
import pyautogui
import time
import sys
import csv
import address_search

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
            zip_code = coord
        else:
            pyautogui.write(coord)
            time.sleep(1)

    return zip_code

def is_int(zip):
    try:
        int(zip)
        return True
    except ValueError:
        return False

def execute(instructions):
    info = read_json(instructions)
    true_zip_code = read_coords(info)
    print('this is repeating')
    if true_zip_code == "" or (isinstance(true_zip_code, int) and true_zip_code != 0):
        pyautogui.moveTo(159, 308, duration=0.2)
        pyautogui.click()
        pyautogui.moveTo(152, 284, duration=0.2)
        pyautogui.click()

        address_search.scan(str(true_zip_code))
    else:
        pyautogui.moveTo(222, 280, duration=0.2)
        pyautogui.click()
        keyboard.write(info[-1])
    

# goes from process_csv

# goes to address_search
