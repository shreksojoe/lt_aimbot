import pyautogui
import pyperclip
import address_search
import win32gui
import keyboard
import time
import json
import csv
import sys
import os
from datetime import datetime

import window
import motion
import data

def csv_rows_to_array(input_csv):
    row_array = []
    with open(input_csv, newline='') as opened_csv:
        reader = csv.reader(opened_csv)
        for row in reader:
            try:
                row_array.append(row)
            except UnicodeDecodeError:
                print("Skipping a row due to UnicodeDecodeError")
                continue
    return row_array

def type_keyboard(text):
    print(f"text: {text}")
    if text is None:
        text = ""
    keyboard.write(str(text))
    time.sleep(0.3)

def check_for_low_stock(indicator):
    print("d4vd", indicator)
    if indicator == 'True': # and prev_row[7] != 'True':
        move_mouse([841, 118])
        time.sleep(0.3)
        move_mouse([729, 171])
        time.sleep(0.3)
    # this is for FBA Low Stock
    elif indicator == 'False':
        move_mouse([841, 118])
        time.sleep(0.3)
        move_mouse([710, 138])
        time.sleep(0.3)

orchestra = {
        "Coordinates": motion.move_abs(value[0], value[1]),
        "Window": window.title_contains(value, process_name),
        "Text": type_keyboard(value),
        "Name": "do nothing",
        "Ship Date": type_keyboard(data.standardize(csv[0][2]))
        "Low Stock": check_for_low_stock(csv_rows[0][7])
        }

def ticket_instructions(csv_rows, json_list):
    for object in json_list:
        print(f"Cycling through objects of json list: {object}")
        for key, value in objects.items():
            print(f"Cycling through key, value pairs of objects: {key}, {value}")

            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)

            print(f"Processing key: {key}, value: {value}")



            orchestra.get[key](value)












