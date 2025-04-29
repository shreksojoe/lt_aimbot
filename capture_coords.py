import pyautogui
import time

print('Move mouse to desired possition and press Enter...')
input("\tReady? Press Enter when your mouse is positioned.")

x, y = pyautogui.position()
print(f"Cursor is at ({x}, {y})")
