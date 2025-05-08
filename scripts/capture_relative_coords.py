import pyautogui
import time
import pygetwindow as gw
import win32gui
import win32con

#print('Move mouse to desired possition and press Enter...')
#input("\tReady? Press Enter when your mouse is positioned.")
#
#x, y = pyautogui.position()
#print(f"Cursor is at ({x}, {y})")

mouse_x, mouse_y = pyautogui.position()

def get_window_under_cursor(mouse_x, mouse_y):
    hwnd = win32gui.WindowFromPoint((mouse_x, mouse_y))
    if hwnd:
        window = gw.Window(hwnd)
        return window
    return None

def click_window(window):
    window.activate()
    pyautogui.click()
    print("Clicked Window", window.title)

def get_relative_coordinates(window, mouse_x, mouse_y):
    left, top = window.left, window.top

    x_relative = mouse_x - left
    y_relative = mouse_y - top
    return x_relative, y_relative

def main():
    print("Move your mouse to desire location, then press 'Enter'")
    window = get_window_under_cursor(mouse_x, mouse_y)

    if window:
        click_window(window)

        x_relative, y_relative = get_relative_coordinates(window, mouse_x, mouse_y)
        print(f"Relative Coordinats: ({x_relative}, {y_relative})")
    else:
        print("No window found under cusor")


main()
