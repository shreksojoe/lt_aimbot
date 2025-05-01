import keyboard
import time
import re
import csv
import pyperclip
import os
import pyautogui

# mouse is already clicked on the right row
# 1. activate down arrow
# 2. move the mouse down by 18px, click
# 3. ctrl + c to extract row
# 4. check zip code (rip this from the ai)
# repeat 1-3 10 times(?) (or untill 2 repeats)
# for the remaining, disgaurd step 2, and go untill 2 orders repeat

def extract_zip(address):
    match = re.search(r'\b\d{5}(?:-\d{4})?\b', address)
    if match:
        return match.group()
    return None

def extract_address():
    with open('csv.txt', 'r') as f:
        address = f.read()
        return address
        os.remove()

def check_dup(prev_row, curr_row):
    if prev_row == curr_row:
        return 1
    else:
        return 0

def compare_zip(zip2):
    zip1 = extract_zip(extract_address())
    if zip1 == zip2:
        return 1
    else: return 0
    
def move_mouse_down():
    x, y = pyautogui.position()
    pyautogui.moveTo(x, y +18)


def loop():
    cache = []
    for i in range(40):
        keyboard.press_and_release('down')

        if i < 10:
            move_mouse_down()

        pyautogui.click()
        keyboard.press_and_release('ctrl+c')
        current_address = pyperclip.paste()

        if compare_zip(extract_zip(current_address)) == 1:
            return
        else:
            cache.append(current_address)
            if check_dup(cache[-1], cache[-2]) == 1:
                return


loop()

