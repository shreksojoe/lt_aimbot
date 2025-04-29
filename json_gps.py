import json
import pyautogui
import time

# read json and return list
def read_json(file_name):
    with open (file_name, 'r') as file:
        data = json.load(file)
        value_list = []
        for element in data:
            #exception "Name"
            for key, value in element. items():
                if key != "Name":
                    value_list.append(value)

        return value_list

def read_coords(instructions):
    for coord in instructions:
        if isinstance(coord, list) and len(coord) == 2 and all(isinstance(x, (int, float)) for x in coord):
            pyautogui.moveTo(coord[0], coord[1], duration=0.2)
            pyautogui.click()
            time.sleep(0.2)
        else:
            pyautogui.write(coord)
            time.sleep(0.2)
if __name__ == "__main__":
    home_btn_info = read_json(r'C:\\Users\Joseph.Stadum\\lt_aimbot\\ticket.json')
    read_coords(home_btn_info)


