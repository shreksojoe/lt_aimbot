import pyautogui
import time
import pygetwindow as gw
import win32gui
import win32con

print('Move mouse to desired possition and press Enter...')
input("\tReady? Press Enter when your mouse is positioned.")

x, y = pyautogui.position()
print(f"Cursor is at ({x}, {y})")
