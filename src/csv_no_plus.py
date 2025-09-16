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
    with open(input_csv, newline='') as opened_csv:
        reader = csv.reader(opened_csv)
        for row in reader:
            try:
                row_array.append(row)
            except UnicodeDecodeError:
                print("Skipping a row due to UnicodeDecodeError")
                continue
    return row_array

def move_mouse(coords):
    pyautogui.moveTo(coords[0], coords[1], duration=0.3)
    pyautogui.click()
    time.sleep(0.5)

def type_keyboard(text):
    print(f"text: {text}")
    # Guard against None and ensure we always write a string
    if text is None:
        text = ""
    keyboard.write(str(text))
    time.sleep(0.3)

# Date formate from YYYY-MM-DD to MM/DD/YYY
def convert_date_format(date_str):
    # Normalize input and strip any time component (e.g., "2025-09-26 23:52:37.038" or ISO "2025-09-26T23:52:37Z")
    date_str = "" if date_str is None else str(date_str).strip()
    date_only = date_str.replace('T', ' ').split(' ')[0]

    formats_to_try = [
        "%Y-%m-%d",  # 2025-04-04
        "%m/%d/%Y",  # 04/04/2025
        "%d-%m-%Y",  # 04-04-2025
        "%Y/%m/%d",  # 2025/04/04
        "%d/%m/%Y",  # 04/04/2025 (common outside US)
        # "%M/%d/%Y",  # Incorrect: %M is minutes; keep for reference
        "%m/%d/%y"  # 04/04/25
    ]
        
    for fmt in formats_to_try:
        try:
            parsed_date = datetime.strptime(date_only, fmt)
            return parsed_date.strftime("%m/%d/%Y")
        except ValueError:
            continue
    # Fallback: if parsing fails, return the original input to avoid NoneType downstream
    return date_only

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
                print(f"Typing customer name: {csv_rows}")
                type_keyboard(csv_rows[0][0])
                time.sleep(0.5)
            elif key == "PO Number":
                print("Typing PO number")
                new_description = csv_rows[0][1]
                type_keyboard(new_description)
                time.sleep(0.5)
            elif key == "Ship Date":
                print(f"Typing ship date: {csv_rows[0][2]}")
                type_keyboard(convert_date_format(csv_rows[0][2]))
                time.sleep(0.5)

# code that repeats each product for each line in the csv. Just now finding out that that is only for a very specific use case. smh
def order_instructions(csv_rows, json_list,  amz_exec):

    # # if it is a file path (for normal csv), turn it into a 2d array
    # if isinstance(user_csv, str):
    #     csv_rows = csv_rows_to_array(user_csv)
    # # if it is  an array (for is_amazon), keep it
    # elif isinstance(user_csv, list):
    #     csv_rows = user_csv

    print(f'csv rows: {csv_rows}')
    print(f'json list: {json_list}')


    # product_ammount = 0
    # if is_amazon == True:
    #     product_amount = 1 
    # else:
    #     product_amount = len(csv_rows)
    # subtract = [833,550]
    # product_ammount_entered = False

    general_desciption_executed = False

    # Process each instruction in sequence
    #for i in range(product_amount):
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
            # archive this bitch
            # elif key == "Coordinates":
            #     if ((value == [834, 353] or value == [885, 364]) and not product_ammount_entered):
            #         move_mouse(value)
            #         time.sleep(0.5)
            #     elif (not value == [834, 353] or value == [885, 364]):
            #         move_mouse(value)
            #         time.sleep(0.5)
            elif key == "Coordinate":
                print(f'moveing mouse to coords: {value}')
                # new_value = value[0], value[1]  22
                move_mouse(value)
                time.sleep(0.5)
            elif key == "Quantity":
                type_keyboard(csv_rows[amz_exec][3])
                time.sleep(0.5)
            elif key == "Product Number":
                print('Product Number evaluated to true')
                print(f'typing... {csv_rows[amz_exec][4]}')
                time.sleep(0.5)
                type_keyboard(csv_rows[amz_exec][4])
                time.sleep(0.5)
            elif (value == "Description Text Box" or value == "General Description Text Box") and general_description_executed == True:
                continue
            elif key == "Copy" and general_desciption_executed == False:
                pyautogui.hotkey('ctrl','c')
                time.sleep(0.3)
            elif key == "Paste"and general_desciption_executed == False:
                general_description = pyperclip.paste()
                type_keyboard(general_description)
                general_desciption_executed = True
            elif key == "Ship Date":
                print(f"Typing ship date: {csv_rows[amz_exec][2]}")
                type_keyboard(convert_date_format(csv_rows[0][2]))
                time.sleep(0.5)


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
            elif key == "Ship Date":
                print(f"Typing ship date: {csv_rows[amz_exec][2]}")
                type_keyboard(convert_date_format(csv_rows[0][2]))
                time.sleep(0.5)

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
                # Originally a try catch for distinguishing between zip (integer) and strings
                type_keyboard(csv_rows[0][6])
                time.sleep(0.5)
                move_mouse(location_coords)
                address_search.scan(str(csv_rows[0][6]))
                time.sleep(0.5)
                move_mouse(ok_button_coords)
            elif key == "Order Notes":
                type_keyboard('Production 1')

def duplicate(csv_rows, relapse_list, amz_exec):

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
            elif key == "Ship Date":
                print(f"Typing ship date: {csv_rows[amz_exec][2]}")
                type_keyboard(convert_date_format(csv_rows[0][2]))
                time.sleep(0.5)
            elif key == "Select All":
                print("Performing select all")
                for _ in range(9):
                    keyboard.send('backspace')
                time.sleep(0.5)

def launch_instructions(user_csv, ticket_array, checkbox_array, order_array, dup_order_array, finish_him_array, duplicate_array, relapse_array):
    csv_rows = csv_rows_to_array(user_csv)
    
    ticket_instructions(csv_rows, ticket_array)
    ticket_instructions(csv_rows, checkbox_array)

    for csv_row in range(len(csv_rows)):
        row = csv_rows[csv_row]

        # disgaurds all rows that have no true or false at the end
        
        # executes the firt time as a setup for the rest of the order
        # csv_row is an integer
        if csv_row == 0: 
            order_instructions(csv_rows, order_array, csv_row)
            finish_him_instructions(csv_rows, finish_him_array)
            continue

        prev_row = csv_rows[csv_row - 1]
        if len(prev_row) >= 8:

            # 'True' determins if the order is an amazon with FBA Low Stock or not

            #   This checks if the csv row before that was a FBA Low Stock, in which case it toggles
            # based on whether or not the current one is FBA Low Stock. 
            if row[7] == 'True': # and prev_row[7] != 'True':
                move_mouse([841, 118])
                move_mouse([729, 171])
                time.sleep(0.3)
            # this is for FBA Low Stock
            elif row[7] == 'False':
                move_mouse([841, 118])
                move_mouse([710, 138])
                time.sleep(0.3)
    

        duplicate(csv_rows, duplicate_array, csv_row)
        duplicate_order(csv_rows[csv_row], dup_order_array, csv_row)

    duplicate(csv_rows, relapse_array)

# code| below triggers the plus funcionalitly, specifically the 0 passed into order_instructions
#     V
    # else:
    #     order_instructions(user_csv, order_array, is_amazon, 0)
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


