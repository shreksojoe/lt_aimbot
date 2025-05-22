import pyautogui
import keyboard
import time
import json
import csv
import sys
import os


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
    pyautogui.typewrite(text)

def csv_into_json(user_csv, user_json):
    csv_rows = csv_rows_to_array(user_csv)
    product_amount = len(csv_rows)
    # Cycle through the JSON file
    # Check the values of the key
    # Add csv elements based on the value of the key
    # Repeat from Quantity Text Box to Price
    # Add objects
    
    # load json file into memory with read permissions
    with open (user_json, 'r') as json_instructions:
        json_step = json.load(json_instructions)
    
        for object in json_step:
            for key, value in object.items():
                for order in csv_rows:
                    # if key == "Name": continue
                        
                    # Start the loop for repeat orders
                    if value == "Quantity Text Box":
                        for product in range(product_amount):
                            type


                    # move mouse and type for the rest
                    elif not key == "Name":
                        if key == "Coordinates": # works
                            move_mouse(value)
                        elif key == "Select All":
                            for _ in range(9):
                                pyautogui.press('backspace')
                        elif not value:
                            type_keyboard(order)




# Take csv and json as input

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






