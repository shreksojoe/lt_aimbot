import json
import keyboard
import pygetwindow as gw
import pyautogui
import time
import sys
import csv
# import address_search


# basic functionality of json_gps:
# coords.json => json_gps
#                   |
#                   v
#     move mouse, click, and keyboard


# read json and return list
def read_json(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        value_list = []
        for element in data:
            #exception "Name"
            for key, value in element.items():
                if key != "Name":
                    value_list.append(value)
    

        return value_list
    except json.JSONDecodeError as e:
        print(f"Error: the file '{filepath}' is not a valid JSON file.\nDetails: {e}")
        return None
    except FileNotFoundError:
        print(f"Error: the file '{filepath}' was not found.")
        return None


def read_coords(instructions):
    if instructions is None:
        print("No instructions to process.")
        return None
    
    print("\n=== Debug: Processing Instructions ===")
    print(f"Type of instructions: {type(instructions)}")
    print(f"Instructions content: {instructions}")
    
    zip_code = 0
    for i, coord in enumerate(instructions):
        print(f"\nProcessing item {i}: {coord} (type: {type(coord)})")

        if isinstance(coord, list) and len(coord) == 2 and all(isinstance(x, (int, float)) for x in coord):
            print(f"  - Found coordinates: {coord}")
            pyautogui.moveTo(coord[0], coord[1], duration=0.2)
            pyautogui.click()
            time.sleep(1)
        elif isinstance(coord, int):
            print(f"  - Found zip code: {coord}")
            zip_code = coord
            
            # Handle zip code based on its type
            if is_int(zip_code):
                print(f"  - {zip_code} is a valid integer. Clicking Location Link and searching address...")
                pyautogui.moveTo(166, 284, duration=0.2)  # Location Link coordinates
                pyautogui.click()
                time.sleep(1)  # Wait for the location link to be clicked
                
                # Import and use address search
                import address_search
                print(f"Launching address search for zip code: {zip_code}")
                address_search.scan(str(zip_code))
            else:
                print(f"  - {zip_code} is not a valid integer. Typing in Location Text Box...")
                pyautogui.moveTo(209, 279, duration=0.2)  # Location Text Box coordinates
                pyautogui.click()
                pyautogui.write(str(zip_code))
            time.sleep(1)
            
        else:
            print(f"  - Found string: '{coord}'. Typing...")
            pyautogui.write(str(coord))
            time.sleep(1)
    
    print(f"\n=== Debug: Final zip code: {zip_code} ===")
    return zip_code

def is_int(zip):
    try:
        int(zip)
        return True
    except ValueError:
        return False

def execute(instructions):
    info = read_json(instructions)
    print(info)
    if info is None:
        print("No valid data to process. Exiting.")
        return
    else:
        true_zip_code = read_coords(info)
    print('this is repeating')
    if true_zip_code == "" or (isinstance(true_zip_code, int) and true_zip_code != 0):
        pyautogui.moveTo(159, 308, duration=0.2)
        pyautogui.click()
        pyautogui.moveTo(152, 284, duration=0.2)
        pyautogui.click()

        #address_search.scan(str(true_zip_code))
    else:
        pyautogui.moveTo(222, 280, duration=0.2)
        pyautogui.click()
        keyboard.write(info[-1])
    
if (len(sys.argv) > 1):
    execute(sys.argv[1])
else:
    print('No file was inputed')


# goes from process_csv

# goes to address_search
