import keyboard
import time
import re
import csv
import pyperclip
import os
import pyautogui
import sys
import json_gps
import login

# mouse is already clicked on the right row
# 1. activate down arrow
# 2. move the mouse down by 18px, click
# 3. ctrl + c to extract row
# 4. check zip code (rip this from the ai)
# repeat 1-3 10 times(?) (or untill 2 repeats)
# for the remaining, disgaurd step 2, and go untill 2 orders repeat

# takes the address (originally from the csv) and converts it into a zip code
def extract_zip(string_address):

    zips = re.findall(r'\b\d{5}(?:-\d{4})?\b', string_address)
    if len(zips) >=2:
        return zips[1]
        print(f"potential first zip from extract_zip: {zips[1]}")
    elif len(zips) == 1:
        return zips[0]
        print(f"potential second zip from extract_zip: {zips[0]}")
    else:
        address = 'AMAZON FBA USA'
        if address in string_address:
            return True
        else: 
            return None

# checks if the last 2 addresses repeated (If it has reached the bottom of the list)
def check_dup(prev_row, curr_row):
    if prev_row == curr_row:
        return 1
    else:
        return 0

# compares the 2 extracted zip codes
def compare_zip(zip1, zip2):
    true_zip = str(zip1) 
    test_zip = str(zip2) 
    if true_zip in test_zip or test_zip in true_zip:
        return 1
    else: return 0
    
# move mouse
time.sleep(0.5)
def move_mouse_down():
    x, y = pyautogui.position()
    pyautogui.moveTo(x, y + 20)

# control loop
def loop(zip_code):
    cache = []
    for i in range(40):
        keyboard.press_and_release('down')

        if i < 9:
            move_mouse_down()
        else:
            print("1-10 failed")
        time.sleep(0.3)

        pyautogui.click()
        time.sleep(0.2)
        pyautogui.hotkey('ctrl','c')
        current_address = pyperclip.paste()
        print(f"current address: {current_address}")

        pyperclip.copy("")
        # not necessarily a zip any more tho
        test_zip_code = extract_zip(current_address)
        print(f"test_zip_code: {test_zip_code}")

        zip_status = 0

        if test_zip_code == True:
            zip_status = 1
            print(f'zip_status is {zip_status}')
        else:
            zip_status = compare_zip(zip_code, test_zip_code)

        if zip_status == 1:
            print("correct address found!")
            return
        else:
            cache.append(current_address)
            current_address = ""
            if len(cache) >= 2 and check_dup(cache[-1], cache[-2]) == 1:
                print("got a repeat")
                return

def json_replacement():
    # Move to Locatin Link
    pyautogui.moveTo(209, 279, duration=0.2)
    pyautogui.click()
    pyautogui.write(str(zip_code))

def scan(addr): 
    # type_shit = login.find_rel_path("json_gps.py", "instructions\type_location.json")

    try:
        zip_code = int(addr)
    except ValueError:
        # json_gps.execute(type_shit)
        keyboard.write(addr)
        zip_code = addr

    # json_replacement()
    print(f"zip code switched to int: {zip_code}")
    zip_code = str(zip_code)
    loop(zip_code)




# 1. Type Zip Code (or whatever value is in that position)
# 2. If it is a Zip Code (and not something like "Amzon FBA"), it should click "Location"
# 3. In the window it opens, it starts at the top of the chart and clicks the first row
# 4. It copys the whole row to the clipboard
# 5. Finds the zip code from the row, and compares that to the zip code from the csv file
# 6. Moves the mouse down and clicks the next row
# 7. Activates the Down Arrow (to highlight the next row)
# 8. Copys that to clipboard
# 9. repeat at step 5 untill it finds a match
# 10. When a match is found it clicks the OK button
