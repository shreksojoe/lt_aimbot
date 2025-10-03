import window
import motion
import data
import importlib.util
import csv
import sys
import os
import json
import keyboard
import time
import pyperclip
import pyautogui
import re
import win32gui

process_name = "Label Traxx Client.exe"
process_path = "C:\Program Files\LT Client\Label Traxx Client.exe"
lt_hwnd = window.get_hwnd(process_name)

def copy():
    time.sleep(1)
    pyautogui.hotkey("ctrl", "c")
    clipboard = pyperclip.paste()
    print("copied: ", clipboard)
    time.sleep(1)

def stock(product):
    print("tis stock: ", product)

def write_zeros(x):
    y = "00000"
    z = 5 - len(x) # ammount of digits
    y[-z] = x
    print(y)
    data.write()
def custom(product, ln):

    def strip_zeros():
        text = pyperclip.paste()
        print("on clipboard: ", text)
        ln_numb = "L#" + str(ln) + " - "
        print("General description: ", ln_numb + text)
        data.write(ln_numb + text)

    print("tis custom: ", product)
    ops = {
            "Coordinate":motion.move_rel,
            "Coordinate Maybe":motion.move_rel,
            "Window":window.title_contains,
            "Window Maybe":window.title_contains_option,
            "Customer Name": lambda: data.write("W.W. Grainger"),
            "PO Number": lambda: data.write(product[1]),
            "Select All": motion.select_all,
            "Ship Date": lambda: data.write(product[5]),
            "Low Stock": lambda: data.write("test"),
            "Quantity": lambda: data.write(product[6]),
            "Product No.": lambda: data.write(product[3]),
            "Price": lambda: data.compare(product[7]),
            "Copy": copy,
            "Line Number": strip_zeros,
            "Line Number Zero": lambda: data.write(str(ln))
            }

    # ops["Airbreakingsystem"](lt_hwnd, 25, 373)

    cust_drop_one = data.find_rel_path("instructions\\cust_drop_one.json")
    cust_drop_two = data.find_rel_path("instructions\\cust_drop_two.json")
    cust_drop_three = data.find_rel_path("instructions\\cust_drop_three.json")
    cust_drop_four = data.find_rel_path("instructions\\cust_drop_four.json")

    with open(cust_drop_one, "r") as file:
        cust_drop_one_data = json.load(file)

    for entry in cust_drop_one_data:
        for key, value in entry.items():
            time.sleep(0.2)

            print(f"Key: {key} -> Value: {value}")
            if isinstance(value, list) :
                if key.endswith("Maybe"):
                    hwnd = win32gui.GetForegroundWindow()
                    ops[key](hwnd, value[0], value[1])
                ops[key](lt_hwnd, value[0], value[1])
            elif key == "Name":
                continue
            elif not value:
                ops[key]()
            else:
                ops[key](value, process_name)

def dropship(product, ln):
    print("Dealing with a dropship")

    stock_product_numbers = [
    "10Y376","8X606","10Y373","8EE38","8E085", "10Y374", "8EEP0", "10Y370", "8E984", "9WA32", "10Y372", "8EE37", "10Y371", "8NCA9", "8AY66", "9WC95", "10Y495"
    ]
    
    if product[3] in stock_product_numbers:
        print("It is a stock product")
        stock(product)
        if not product[8] == "iStock":
            print(product[8])
            product[8] = "iStock"
        print(product[8])
    else:
        print("this is a custom product")
        print(product[8])

        if not product[8] == "Custom":
            print(product[8])
            product[8] = "Custom"
            custom(product, ln)
        print(product[8])

        # in grainger_instructions: line 47 custom products, 

def execute_grainger(grainger_pdf):
    pdf_path = data.find_rel_path(r"pdf_to_csv\\main.py")
    
    # Add pdf_to_csv directory to sys.path so imports work
    pdf_dir = os.path.dirname(pdf_path)
    if pdf_dir not in sys.path:
        sys.path.insert(0, pdf_dir)

    spec = importlib.util.spec_from_file_location("pdf_module", pdf_path)
    pdf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pdf_module)
    
    print("Converting PDF to CSV and processing...")
    # main.py.convert() returns the 2D array from csv_sort.process_file()
    product_array = pdf_module.convert(grainger_pdf)
    
    print(f"Processed {len(product_array)} product(s) from Grainger PDF")
    for ln, product in enumerate(product_array):
        print(product)
        # determine if it is a grainger or dropship
        if not ("grainger" in product[-1].lower()): # it is a dropship
            print("grainger isn't in the address, tis a dropship")
            dropship(product, ln + 1)
        else: # it is a grainger
            print("it was an grainger dammit")
    
    return product_array
