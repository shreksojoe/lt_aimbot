import json
import pyautogui
import keyboard
import time
# Forbidden Values!


def navigate_ticket(array_of_instructions):
    for row in array_of_instructions:  # Each row is a dictionary
        for key, value in row.items():  # Iterate over dictionary items
            if key == "Name":
                continue
            elif key == "Coordinates":  # Fixed typo from "Coordinate" to "Coordinates"
                pyautogui.moveTo(value[0], value[1])
                pyautogui.click()
                time.sleep(0.2)
            elif key == "Select All":  # Check the key, not the value
                for _ in range(9):
                    keyboard.send('backspace')
            else:
                keyboard.type(str(value))  # Ensure value is converted to string






