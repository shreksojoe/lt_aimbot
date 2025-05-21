import pyautogui
import keyboard
import time
import json
import csv
import sys
import os

# Global variables:
ticket_structure_is_done = False

# Opens the csv, and stores rows in array 
def csv_rows_to_array(input_csv):
    row_array = []
    with open(input_csv, newline = '') as opened_csv:
        reader = csv.reader(opened_csv)
        for row in reader:
            row_array.append(row)
    return row_array

def move_mouse(coords):
    pyautogui.moveTo(coords[0], coords[1])
    pyautogui.click()
    time.sleep(0.2)

def type_keyboard(text):
    keyboard.write(text)
    time.sleep(0.2)

def make_ticket_structure(key, value, element):
    print(f"key after testing: {key}")
    print(f"value after testing: {value}")
    if key == "Coordinates": # works
        move_mouse(value)
        time.sleep(0.5)
    elif key == "Select All":
        for _ in range(9):
            pyautogui.press('backspace')
        time.sleep(0.2)
        action_is_done = True
    elif not value:
        print(f"just about to print: {element}")
        type_keyboard(element)
        action_is_done = True
    else:
        ticket_structure_is_done = True
        print(f"ticket struct: {ticket_structure_is_done}")

def csv_into_json(user_csv, user_json):
    action_is_done = False
    csv_rows = csv_rows_to_array(user_csv)
    product_amount = len(csv_rows)
    json_objects = []
    # Cycle through the JSON file
    # Check the values of the key
    # Add csv elements based on the value of the key
    # Repeat from Quantity Text Box to Price
    # Add objects
    
    # load json file into memory with read permissions
    with open (user_json, 'r') as json_instructions:
        json_step = json.load(json_instructions)
    
        for object in json_step: # repeats for every single step in the .json file
            action_is_done = False
            for key, value in object.items(): # this repeats for every element in each line
                print(f"key: {key}, value:{value}")
                # json_objects.append(f'{key}:{value}')
                for order in csv_rows: # first loops through the order (x2)
                    for element in order:

                        # Handle multiple orders
                        if value == "Quantity Text Box":
                            for product in range(product_amount):
                                type
                                action_is_done = True

                        elif not (key == "Name" and ticket_structure_is_done):
                            make_ticket_structure(key, value, element)
                            break
                        else: 
                            break

            if action_is_done:
                break
                
        print(f"json_objects: {order}")




# Take csv and json as input
def cli_aimbot(cvs_file, json_file):

    if (not sys.argv[1].strip('"').endswith('.csv')):
        print('First file is not a csv. Exiting ...')
        sys.exit()

    if (not sys.argv[2].endswith('.json')):
        print('Second file is not a json. Exiting ...')
        sys.exit()

    csv_into_json(sys.argv[1],sys.argv[2])

if __name__ == "__main__":
    cli_aimbot(sys.argv[1], sys.argv[2])

# We have now determined that we have a csv and json file
# We need to add the csv elements to the json file
# 1. Cycle through csv
# 2. Cycle through json
# 3. 






