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

def csv_to_array(user_csv):
    csv_array = []
    with open (user_csv, newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader: 
            csv_array.append(row)
    return csv_array

def make_ticket_structure(json_key, json_value, csv_row):
    """Process a single field using the current CSV row data"""
    if json_key == "Coordinates":
        move_mouse(json_value)
        time.sleep(0.5)
    elif json_key == "Customer Name":
        type_keyboard(csv_row[0] if len(csv_row) > 0 else "")
    elif json_key == "PO Number":
        type_keyboard(csv_row[1] if len(csv_row) > 1 else "")
    elif json_key == "Select All":
        for _ in range(9):
            pyautogui.press('backspace')
        time.sleep(0.2)
    elif json_key == "Ship Date":
        type_keyboard(csv_row[2] if len(csv_row) > 2 else "")
    elif json_key == "Quantity":
        type_keyboard(csv_row[3] if len(csv_row) > 3 else "")
    elif json_key == "Product Number":
        type_keyboard(csv_row[4] if len(csv_row) > 4 else "")
    elif json_key == "Price":
        type_keyboard(csv_row[5] if len(csv_row) > 5 else "")
    elif json_key == "Zip":
        type_keyboard(csv_row[6] if len(csv_row) > 6 else "")
    elif json_key == "Order Notes":
        type_keyboard(csv_row[7] if len(csv_row) > 7 else "")

# Turns the csv file into an array
def get_instruction_array(user_json):
    with open(user_json, 'r') as json_instructions:
        return json.load(json_instructions)

def process_instructions(instructions, csv_data):
    """Process a single CSV row through all instructions"""
    for instruction in instructions:
        if "Name" in instruction and "Coordinates" in instruction:
            # This is a clickable element (button, link, etc.)
            print(f"Clicking: {instruction['Name']} at {instruction['Coordinates']}")
            move_mouse(instruction["Coordinates"])
            time.sleep(0.5)
            pyautogui.click()
            time.sleep(0.5)
        elif any(key in instruction for key in ["Customer Name", "PO Number", "Select All", "Ship Date", 
                                              "Quantity", "Product Number", "Price", "Zip", "Order Notes"]):
            # This is a text field that needs data from CSV
            for key in instruction:
                if key in ["Customer Name", "PO Number", "Select All", "Ship Date", 
                         "Quantity", "Product Number", "Price", "Zip", "Order Notes"]:
                    print(f"Processing {key} for current CSV row")
                    make_ticket_structure(key, instruction[key], csv_data)
                    time.sleep(0.3)

def add_csv_elements(user_json, user_csv):
    # First, load all CSV data
    with open(user_csv, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        csv_data = list(csv_reader)  # Read all rows into memory
    
    # Load instructions
    instructions = get_instruction_array(user_json)
    
    # Process each CSV row one at a time
    for row in csv_data:
        print(f"\nProcessing CSV row: {row}")
        # Process all instructions for this CSV row
        process_instructions(instructions, row)
        
        # Add a pause between processing different CSV rows
        time.sleep(1.0)

# def csv_into_json(user_csv, user_json):

#    add_csv_elements(user_json, user_csv)


    # action_is_done = False
    # csv_rows = csv_rows_to_array(user_csv)
    # product_amount = len(csv_rows)
    # json_objects = []

    # We now have an array of json instructions
    # Can access key and value at the same time
    # Read this

    # functionality for make_ticket_structure
    # If Key = Coordinates, execute coordinates
    # If Key = "Name" skip
    # If Key = anything else, type
    # 
    # Core functionality: when something happens in json instrucions, do something with csv element
    
        # for order in csv_rows: # first loops through the order (x2)
        #     for element in order:
        #         # print(f"element: {element}")
        #         # Handle multiple orders
        #         if value == "Quantity Text Box":
        #             for product in range(product_amount):
        #                 type
        #                 action_is_done = True

        #         elif not (key == "Name" and ticket_structure_is_done):
        #             make_ticket_structure(key, value, element)
        #             continue

        #     make_ticket_structure_is_done = True


# Take csv and json as input
def cli_aimbot(cvs_file, json_file):

    if (not sys.argv[1].strip('"').endswith('.csv')):
        print('First file is not a csv. Exiting ...')
        sys.exit()

    if (not sys.argv[2].endswith('.json')):
        print('Second file is not a json. Exiting ...')
        sys.exit()

    add_csv_elements(sys.argv[1],sys.argv[2])

if __name__ == "__main__":
    cli_aimbot(sys.argv[1], sys.argv[2])

# We have now determined that we have a csv and json file
# We need to add the csv elements to the json file
# 1. Cycle through csv
# 2. Cycle through json
# 3. 






