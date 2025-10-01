import motion
import window
import data
# fuck abs, we're going to do:
import json
import keyboard

process_name = "Label Traxx Client.exe"
process_path = "C:\Program Files\LT Client\Label Traxx Client.exe"
lt_hwnd = window.get_hwnd(process_name)

ops = {
        "Coordinate":motion.move_rel,
        "Window":window.title_contains,
        "Customer Name": lambda: keyboard.write(),
        "PO Number": lambda: keyboard.write("W.W. Grainger"),
        "Select All": lambda: keyboard.write(),
        "Ship Date": lambda: keyboard.write(),
        "Low Stock": lambda: keyboard.write
        }

# ops["Airbreakingsystem"](lt_hwnd, 25, 373)

json_file = data.find_rel_path("instructions\\cust_drop_one.json")

with open(json_file, "r") as file:
    data = json.load(file)

for entry in data:
    for key, value in entry.items():

        print(f"Key: {key} -> Value: {value}")
        print("lenghthththththt", len(value))
        if isinstance(value, list):
            ops[key](lt_hwnd, value[0], value[1])
        elif key == "Name":
            continue
        elif not value:
            ops[key]()
        else:
            ops[key](value, process_name)
# What your going to be doing:
#  
# looping through the json
# move coordinates accordingly
# not actually looping through the csv, simply accessing specific elementws of it
# you are doing line by line rather than order by order
#
#
#
#
#
#
#
#
#
#
#
#
