import pyautogui
import address_search
import keyboard
import time
import json
import csv
import sys
import os

# location variables:

ticket_json = "instructions\\ticket.json"
order_json = "instructions\\order.json"

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

def ticket_instructions(user_csv, json_list):
    csv_rows = csv_rows_to_array(user_csv)

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
                type_keyboard(csv_rows[0][0])
                time.sleep(0.5)
            elif key == "PO Number":
                print("Typing PO number")
                type_keyboard(csv_rows[0][1])
                time.sleep(0.5)
            elif key == "Ship Date":
                print("Typing ship date")
                type_keyboard(csv_rows[0][2])
                time.sleep(0.5)
             
def order_instructions(user_csv, json_list):
    csv_rows = csv_rows_to_array(user_csv)
    product_amount = len(csv_rows)
    # subtract = [833,550]
    product_ammount_entered = False

    # Process each instruction in sequence
    for i in range(product_amount):
        print(f"i: {i}")
        for object in json_list:
            for key, value in object.items():
                if key == "Name": 
                    continue
                if key == "Coordinates":
                    if (value == [834, 353] or value == [885, 364]) and not product_ammount_entered:
                        move_mouse(value)
                        time.sleep(0.5)
                        product_ammount_entered = True
                    elif not value == [834, 353]:
                        move_mouse(value)
                        time.sleep(0.5)
                if key == "Coordinate":
                    # value[1] + (i * 22)
                    new_value = value[0], value[1] + (i * 22)
                    move_mouse(new_value)
                    time.sleep(0.5)
                elif key == "Quantity":
                    type_keyboard(csv_rows[i][3])
                    time.sleep(0.5)
                elif key == "Product Number":
                    print(f"product # {i}: {csv_rows[i][4]}")
                    time.sleep(0.5)
                    type_keyboard(csv_rows[i][4])
                    time.sleep(0.5)
                elif key == "Price":
                    type_keyboard(csv_rows[i][5])
                    time.sleep(0.5)
                elif key == "Order Amount" and not product_ammount_entered:
                    type_keyboard(product_amount)
                    time.sleep(0.5)

def finish_him_instructions(user_csv, finish_him_list):
    csv_rows = csv_rows_to_array(user_csv)
    location_coords = [157, 281]
    ok_button_coords = [861, 510]

    # Process each instruction in sequence
    for object in finish_him_list:
        for key, value in object.items():
            if key == "Name":
                continue
            if key == "Coordinates":
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



            

def launch_instructions(user_csv, ticket_array, order_array, finish_him_array):
    ticket_instructions(user_csv, ticket_array)
    order_instructions(user_csv, order_array)
    finish_him_instructions(user_csv, finish_him_array)
    
    
            
            # After each action, wait a bit
            # time.sleep(0.2)
#def ticket_instructions(user_csv, json_list):
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

    ticket_instructions(sys.argv[1],sys.argv[2])

# We have now determined that we have a csv and json file
# We need to add the csv elements to the json file
# 1. Cycle through csv
# 2. Cycle through json
# 3. 






