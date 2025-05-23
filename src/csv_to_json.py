import pyautogui
import keyboard
import time
import json
import csv
import sys
import os


# Opens the csv, and stores rows in array 
def csv_rows_to_array(input_csv):
    item_array = []
    with open(input_csv, newline = '') as opened_csv:
        reader = csv.reader(opened_csv)
        for row in reader:
            for item in row:
                item_array.append(item)
    return item_array 

def move_mouse(coords):
    pyautogui.moveTo(coords[0], coords[1])
    pyautogui.click()
    time.sleep(0.1)

def type_keyboard(text):
    keyboard.write(text)
    time.sleep(0.1)

def csv_into_json(user_csv, json_list):
    csv_rows = csv_rows_to_array(user_csv)
    product_amount = len(csv_rows)
    
    # Process each instruction in sequence
    for object in json_list:
        for key, value in object.items():
            print(f"Processing - key: {key}, value: {value}")
            
            # Skip name keys as they're just labels
            if key == "Name":
                continue
                
            # Handle each action
            if key == "Coordinates":
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
                type_keyboard(csv_rows[0])
                time.sleep(0.5)
            elif key == "PO Number":
                print("Typing PO number")
                type_keyboard(csv_rows[1])
                time.sleep(0.5)
            elif key == "Ship Date":
                print("Typing ship date")
                type_keyboard(csv_rows[2])
                time.sleep(0.5)
            
            # After each action, wait a bit
            time.sleep(0.2)
#def csv_into_json(user_csv, json_list):
#    csv_rows = csv_rows_to_array(user_csv)
#    product_amount = len(csv_rows)
#    # Cycle through the JSON file
#    # Check the values of the key
#    # Add csv elements based on the value of the key
#    # Repeat from Quantity Text Box to Price
#    # Add objects
#    
#    # load json file into memory with read permissions
#    #with open (user_json, 'r') as json_instructions:
#    #    json_step = json.load(json_instructions)
#    #
#    for object in json_list:
#         for key, value in object.items():
#
#             print(f"key: {key}, value: {value}")            
#
#             # move mouse and type for the rest
#             if key == "Name":
#                 continue
#             elif key == "Coordinates": # works
#                 move_mouse(value)
#                 time.sleep(0.1)
#                 continue
#             elif key == "Select All":
#                 for _ in range(9):
#                     pyautogui.press('backspace')
#                 time.sleep(0.1)
#                 continue
#             elif key == "Customer Name":
#                 value = csv_rows[0]
#                 type_keyboard(value)
#                 time.sleep(0.1)
#                 continue
#             elif key == "PO Number":
#                 value = csv_rows[1]
#                 type_keyboard(value)
#                 time.sleep(0.1)
#                 continue
#             elif key == "Ship Date":
#                 value = csv_rows[2]
#                 type_keyboard(value)
#                 time.sleep(0.1)
#                 continue
#    print(f"json list: {json_list}")            
#    for biatch in csv_rows:
#        print(f"biatch: {biatch}")
#
#    # Loop through list
#    # for objects in json_list:
#    #     for key, value in objects.items():
#
#    #         if key == "Name":
#    #             continue
#    #         elif key == "Coordinate":
#    #             move_mouse(value)
#    #         elif key == "Select All":
#    #             for _ in range(9):
#    #                 keyboard.send('backspace')
#    #         elif not value:
#    #             type_keyboard(value)
    

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

    csv_into_json(sys.argv[1],sys.argv[2])

# We have now determined that we have a csv and json file
# We need to add the csv elements to the json file
# 1. Cycle through csv
# 2. Cycle through json
# 3. 






