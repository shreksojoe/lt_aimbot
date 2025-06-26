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

# new csv_to_json file with no multiple orders on the same ticket

# Opens the csv, and stores rows in array 
def csv_rows_to_array(input_csv):
    row_array = []
    with open(input_csv, newline = '') as opened_csv:
        reader = csv.reader(opened_csv)
        for row in reader:
            row_array.append(row)
    return row_array 

def move_mouse(coords):
    pyautogui.moveTo(coords[0], coords[1], duration=0.3)
    pyautogui.click()
    time.sleep(0.5)

def type_keyboard(text):
    keyboard.write(text)
    print(f"text: {text}")
    time.sleep(0.3)

# Date formate from YYYY-MM-DD to MM/DD/YYY
def convert_date_format(date_str):
    formats_to_try = [
        "%Y-%m-%d",  # 2025-04-04
        "%m/%d/%Y",  # 04/04/2025
        "%d-%m-%Y",  # 04-04-2025
        "%Y/%m/%d",  # 2025/04/04
        "%d/%m/%Y",  # 04/04/2025 (common outside US)
        "%m/%d/%y",  # 04/04/25
    ]
        
    for fmt in formats_to_try:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.strftime("%m/%d/%Y")
        except ValueError:
            continue

    raise ValueError(f"Unrecognized date format: {date_str}")

# does this repeat for each line in the csv?
def ticket_instructions(csv_rows, json_list):
    
    # Process each instruction in sequence
    for object in json_list:
        print(f'Cycling thorugh objects of json list: {object}')
        for key, value in object.items():
            print(f'Cycling thorugh key, value pairs of objects: {key}, {value}')
            
            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)

            print(f"Processing - key: {key}, value: {value}")
            
            # Skip name keys as they're just labels
            if key == "Name":
                continue
            if key == "Window":
                print(f"title: {title} should contain: {value}")
                first_time = True
                while value not in title:
                    if first_time:
                        print('Program paused because pop up window...')
                    first_time = False
                    hwnd = win32gui.GetForegroundWindow()
                    title = win32gui.GetWindowText(hwnd)
                    time.sleep(1)
            # Handle each action
            elif key == "Coordinates":
                print(f"Moving mouse to coordinates: {value}")
                move_mouse(value)
                time.sleep(0.5)  # Increased sleep time for reliability
            elif key == "Select All":
                print("Performing select all")
                for _ in range(9):
                    keyboard.send('backspace')
                time.sleep(0.5)
            elif key == "Customer Name":
                print("Typing customer name")
                type_keyboard(csv_rows[0][0])
                time.sleep(0.5)
            elif key == "PO Number":
                print("Typing PO number")
                type_keyboard(csv_rows[0][1])
                time.sleep(0.5)
            elif key == "Ship Date":
                print(f"Typing ship date: {csv_rows[0][2]}")
                type_keyboard(convert_date_format(csv_rows[0][2]))
                time.sleep(0.5)

# code that repeats each product for each line in the csv. Just now finding out that that is only for a very specific use case. smh
def order_instructions(csv_rows, json_list, chromalabel, amz_exec):

    # # if it is a file path (for normal csv), turn it into a 2d array
    # if isinstance(user_csv, str):
    #     csv_rows = csv_rows_to_array(user_csv)
    # # if it is  an array (for chromalabel), keep it
    # elif isinstance(user_csv, list):
    #     csv_rows = user_csv


    product_ammount = 0
    if chromalabel == True:
        product_amount = 1 
    else:
        product_amount = len(csv_rows)
    # subtract = [833,550]
    product_ammount_entered = False
    general_desciption_executed = False

    # Process each instruction in sequence
    for i in range(product_amount):

        # other words amz_exec is never i -_-
        # if amz_exec == 0:
        #     amz_exec = i
        
        print(f"i: {amz_exec}")
        for object in json_list:
            for key, value in object.items():


                hwnd = win32gui.GetForegroundWindow()
                title = win32gui.GetWindowText(hwnd)
                print(f"Processing - key: {key}, value: {value}")
                
                if key == "Name": 
                    continue
                if key == "Window":
                    first_time = True
                    print(f"title: |{title} sould contain: {value}")
                    if "Warning" in title :
                        move_mouse([514, 292])
                    while value not in title:
                        if first_time:
                            print('Program paused because pop up window...')
                        first_time = False
                        hwnd = win32gui.GetForegroundWindow()
                        title = win32gui.GetWindowText(hwnd)
                        time.sleep(1)
                elif key == "Coordinates":
                    if ((value == [834, 353] or value == [885, 364]) and not product_ammount_entered):
                        move_mouse(value)
                        time.sleep(0.5)
                    elif (not value == [834, 353] or value == [885, 364]):
                        move_mouse(value)
                        time.sleep(0.5)
                elif key == "Coordinate":
                    # value[1] + (i * 22)
                    new_value = value[0], value[1] + (amz_exec * 22)
                    move_mouse(new_value)
                    time.sleep(0.5)
                elif key == "Quantity":
                    type_keyboard(csv_rows[amz_exec][3])
                    time.sleep(0.5)
                elif key == "Product Number":
                    print(f"product # {i}: {csv_rows[i][4]}")
                    time.sleep(0.5)
                    type_keyboard(csv_rows[amz_exec][4])
                    time.sleep(0.5)
                # elif key == "Price":
                #     type_keyboard(csv_rows[i][5])
                #     time.sleep(0.5)
                elif key == "Order Amount" and not product_ammount_entered:
                    print(len(csv_rows))
                    if chromalabel == True:
                        print("chroma be true")
                        type_keyboard(str(0))
                        time.sleep(0.5)
                        product_ammount_entered = True
                    else:
                        print("chroma be false")
                        type_keyboard(str(len(csv_rows) - 1))
                        time.sleep(0.5)
                        product_ammount_entered = True
                elif (value == "Description Text Box" or value == "General Description Text Box") and general_description_executed == True:
                    continue
                elif key == "Copy" and general_desciption_executed == False:
                    pyautogui.hotkey('ctrl','c')
                    time.sleep(0.3)
                elif key == "Paste"and general_desciption_executed == False:
                    general_description = pyperclip.paste()
                    type_keyboard(general_description)
                    general_desciption_executed = True


def duplicate_order(csv_rows, dup_order_array, amz_exec):

    # subtract = [833,550]
    print(f"csv rows: {csv_rows}")
    product_ammount_entered = False
    general_desciption_executed = False


    # Process each instruction in sequence
    for object in dup_order_array:
        for key, value in object.items():


            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)
            print(f"Processing - key: {key}, value: {value}")
            
            if key == "Name": 
                continue
            if key == "Window":
                first_time = True
                print(f"title: {title} sould contain: {value}")
                if "Warning" in title :
                    move_mouse([514, 292])
                while value not in title:
                    if first_time:
                        print('Program paused because pop up window...')
                    first_time = False
                    hwnd = win32gui.GetForegroundWindow()
                    title = win32gui.GetWindowText(hwnd)
                    time.sleep(1)
            elif key == "Coordinate":
                move_mouse(value)
                time.sleep(0.5)
            elif key == "Quantity":
                type_keyboard(csv_rows[3])
                time.sleep(0.5)
            elif key == "Product Number":
                time.sleep(0.5)
                type_keyboard(csv_rows[4])
                time.sleep(0.5)
            # elif key == "Order Amount" and not product_ammount_entered:
            #     type_keyboard(str(0))
            #     time.sleep(0.5)
            #     product_ammount_entered = True
            elif (value == "Description Text Box" or value == "General Description Text Box") and general_description_executed == True:
                continue
            elif key == "Copy" and general_desciption_executed == False:
                pyautogui.hotkey('ctrl','c')
                time.sleep(0.3)
            elif key == "Paste" and general_desciption_executed == False:
                pyautogui.press('end')
                time.sleep(0.5)
                for _ in range(150):
                    keyboard.send('backspace')
                time.sleep(0.5)
                print('paste: ')
                type_keyboard(pyperclip.paste())
                time.sleep(0.5)
                general_desciption_executed = True

def finish_him_instructions(csv_rows, finish_him_list):
    location_coords = [157, 281]
    ok_button_coords = [861, 510]

    # Process each instruction in sequence
    for object in finish_him_list:
        for key, value in object.items():

            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)
            print(f"Processing - key: {key}, value: {value}")

            if key == "Name":
                continue
            if key == "Window":
                first_time = True

                print(f"title: {title} sould contain: {value}")
                if "Warning" in title :
                    move_mouse([514, 292])
                if first_time:
                    print('Program paused because pop up window...')
                first_time = False
                while value not in title:
                    print('Program paused because pop up window...')
                    hwnd = win32gui.GetForegroundWindow()
                    title = win32gui.GetWindowText(hwnd)
                    time.sleep(1)
            elif key == "Coordinates":
                move_mouse(value)
                time.sleep(0.5)
            elif key == "Zip":
                try:
                    int(csv_rows[0][6])
                    type_keyboard(csv_rows[0][6])
                    time.sleep(0.5)
                    move_mouse(location_coords)
                    address_search.scan(str(csv_rows[0][6]))
                    time.sleep(0.5)
                    move_mouse(ok_button_coords)
                except ValueError:
                    type_keyboard(csv_rows[0][6])
                    time.sleep(0.5)
            elif key == "Order Notes":
                try:
                    type_keyboard(csv_rows[0][7])
                    time.sleep(0.5)
                except IndexError:
                    continue

def duplicate(csv_rows, relapse_list):

    # Process each instruction in sequence
    for object in relapse_list:
        for key, value in object.items():

            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)

            print(f"Processing - key: {key}, value: {value}")
            
            # Skip name keys as they're just labels
            if key == "Name":
                continue
            if key == "Window":
                print(f"title: {title} sould contain: {value}")
                if "Warning" in title :
                    move_mouse([514, 292])
                first_time = True
                while value not in title:
                    if first_time:
                        print('Program paused because pop up window...')
                    first_time = False
                    hwnd = win32gui.GetForegroundWindow()
                    title = win32gui.GetWindowText(hwnd)
                    time.sleep(1)
                
            # Handle each action
            elif key == "Coordinates":
                print(f"Moving mouse to coordinates: {value}")
                move_mouse(value)
                time.sleep(0.5)  # Increased sleep time for reliability

def launch_instructions(user_csv, ticket_array, checkbox_array, order_array, dup_order_array, finish_him_array, duplicate_array, relapse_array, chromalabel):
    csv_rows = csv_rows_to_array(user_csv)

    ticket_instructions(csv_rows, ticket_array)
    ticket_instructions(csv_rows, checkbox_array)

    print(f"user csv: {len(user_csv)}")
    print(f"csv rows (from launch): {len(csv_rows)}")
    # if chromalabel == True:  nah this is always true
    print(f"seventh row: {len(csv_rows)}")
    for csv_row in range(len(csv_rows)):
        row = csv_rows[csv_row]
        print(f'here is the length of each row: {len(row)}')

        if len(row) < 8: 
            continue
        
        # executes the firt time as a setup for the rest of the order
        if csv_row == 0: 
            order_instructions(csv_rows, order_array, chromalabel, csv_row)
            finish_him_instructions(csv_rows, finish_him_array)

        else: 
            prev_row = csv_rows[csv_rows -1]
            if len(prev_row) >= 8:
                if row[7] == 'True' and prev_row[7] != 'True':
                    move_mouse([841, 118])
                    move_mouse([729, 171])
                    time.sleep(0.3)

        if row[7] == 'False':
            move_mouse([841, 118])
            move_mouse([710, 138])
            time.sleep(0.3)

        duplicate(csv_rows, duplicate_array)
        duplicate_order(csv_rows[csv_row], dup_order_array, csv_row)

    duplicate(csv_rows, relapse_array)

# code| below triggers the plus funcionalitly, specifically the 0 passed into order_instructions
#     V
    # else:
    #     order_instructions(user_csv, order_array, chromalabel, 0)
    #     finish_him_instructions(user_csv, finish_him_array)
    #     duplicate(user_csv, relapse_array)
        
        
    
    

# Take csv and json as input
if __name__ == "__main__":
    if (len(sys.argv) <= 2):
        print('Did not input enough files. Exiting ...')
        sys.exit()

    if (not sys.argv[1].strip('"').endswith('.csv')):
        print('First file is not a csv. Exiting ...')
        sys.exit()

    if (not sys.argv[2].endswith('.json')):
        print('Second file is not a json. Exiting ...')
        sys.exit()

    ticket_instructions(sys.argv[1],sys.argv[2])

# We have now determined that we have a csv and json file
# We need to add the csv elements to the json file
# 1. Cycle through csv
# 2. Cycle through json
# 3. 


