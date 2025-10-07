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


stock_product_numbers = [
"10Y376","8X606","10Y373","8EE38","8E085", "10Y374", "8EEP0", "10Y370", "8E984", "9WA32", "10Y372", "8EE37", "10Y371", "8NCA9", "8AY66", "9WC95", "10Y495"
]

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

def move_down(i):
    time.sleep(1)
    for _ in range(i): 
        time.sleep(1)
        pyautogui.press('down')
    keyboard.press_and_release("enter")
    time.sleep(1)
    # pyautogui.click()


def strip_zeros(text):

    if isinstance(text, str):
        # Split on commas and strip spaces
        text = [t.strip() for t in text.split(",") if t.strip()]

    stripped = [str(int(num)) for num in text if num.strip().isdigit()]

    joined = ",".join(stripped)
    string = f"L#{joined} - "

    desc = pyperclip.paste()
    print("On clipboard:", desc)
    gen_desc = string + desc
    print("General description:", gen_desc)

    if 'data' in globals():
        data.write(gen_desc)
    else:
        print("Warning: 'data' file handle not found. Skipping write.")

    return gen_desc

def multiple_prod(products):
    dup_order_data = data.load_file(data.find_rel_path("instructions\\dup_order.json"))

    dups = {
            "Coordinate": motion.move_rel,
            "Window": window.title_contains,
            "Product Ammount":data.write(str(len(products)))
            }

def custom(product, grainger_pdf):

    product[6] = str(int(product[6]) + 30)

    # def strip_zeros():
    #     result = product[2].lstrip("0")
    #     text = pyperclip.paste()
    #     print("on clipboard: ", text)
    #     ln_numb = "L#" + result + " - "
    #     print("General description: ", ln_numb + text)
    #     data.write(ln_numb + text)

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
            "Line Number": lambda: strip_zeros(product[2]),
            "Line Number Zero": lambda: data.write(product[2]),
            "Move Down": lambda: move_down(2),
            "Click": lambda: pyautogui.click()
            }

    # ops["Airbreakingsystem"](lt_hwnd, 25, 373)

    cust_drop_one_data = data.load_file(data.find_rel_path("instructions\\cust_drop_one.json"))
    cust_drop_two_data = data.load_file(data.find_rel_path("instructions\\cust_drop_two.json"))
    cust_drop_three_data = data.load_file(data.find_rel_path("instructions\\cust_drop_three.json"))
    cust_drop_four_data = data.load_file(data.find_rel_path("instructions\\cust_drop_four.json"))
    grainger_address_data = data.load_file(data.find_rel_path("instructions\\grainger_address.json"))
    
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

    if int(product[6]) < 30:
        for entry in cust_drop_two_data:
            for key, value in entry.items():
                if isinstance(value, list):
                    if key.endswith("maybe"):
                        hwnd = win32gui.GetForegroundWindow()
                        ops[key](hwnd, value[0], value[1])
                    ops[key](lt_hwnd, value[0], value[1])
                elif key == "Name":
                    continue
                elif not value:
                    ops[key]()
                else:
                    ops[key](value, process_name)
    else:
        for entry in cust_drop_three_data:
            for key, value in entry.items():
                if isinstance(value, list):
                    if key.endswith("maybe"):
                        hwnd = win32gui.GetForegroundWindow()
                        ops[key](hwnd, value[0], value[1])
                    ops[key](lt_hwnd, value[0], value[1])
                elif key == "Name":
                    continue
                elif not value:
                    ops[key]()
                else:
                    ops[key](value, process_name)

    time.sleep(2)

    for entry in cust_drop_four_data:
        for key, value in entry.items():
            if isinstance(value, list):
                if key.endswith("maybe"):
                    hwnd = win32gui.GetForegroundWindow()
                    ops[key](hwnd, value[0], value[1])
                ops[key](lt_hwnd, value[0], value[1])
            elif key == "Name":
                continue
            elif not value:
                ops[key]()
            else:
                ops[key](value, process_name)

    data.address_search("Grainger Dropship Acct")

    address_array = data.split_addr(product[9])

    def type_address(address):
        for segment in address:
            data.write(segment)
            time.sleep(1)
            keyboard.press_and_release("tab")
            time.sleep(1)

    addr = {
            "Coordinate":motion.move_rel,
            "Coordinate Maybe":motion.move_rel,
            "Window":window.title_contains,
            "Window Maybe":window.title_contains_option,
            "File Name": lambda: data.write(data.swap_slash(grainger_pdf)),
            "Address": lambda: type_address(address_array)
            }

    for entry in grainger_address_data:
        for key, value in entry.items():
            if isinstance(value, list):
                if key.endswith("maybe"):
                    hwnd = win32gui.GetForegroundWindow()
                    addr[key](hwnd, value[0], value[1])
                addr[key](lt_hwnd, value[0], value[1])
            elif key == "Name":
                continue
            elif not value:
                addr[key]()
            else:
                addr[key](value, process_name)

def stock(stock_list):
    if not stock_list: return False

    istock_two_data = data.load_file(data.find_rel_path("instructions\\istock_two.json"))

    for product in stock_list:

        for entry in istock_two_data:
            for key, value in entry.items():
                if isinstance(value, list):
                    if key.endswith("maybe"):
                        hwnd = win32gui.GetForegroundWindow()
                        addr[key](hwnd, value[0], value[1])
                    addr[key](lt_hwnd, value[0], value[1])
                elif key == "Name":
                    continue
                elif not value:
                    addr[key]()
                else:
                    addr[key](value, process_name)

def dropship(product, grainger_pdf):
    print("Dealing with a dropship")

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
        if int(product[2]) > 1:
            motion.move_rel(lt_hwnd, 494, 425)
            time.sleep(0.1)
        custom(product, grainger_pdf)
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

    stock_list = []
    
    print("Converting PDF to CSV and processing...")
    # main.py.convert() returns the 2D array from csv_sort.process_file()
    product_array = pdf_module.convert(grainger_pdf)
    
    print(f"Processed {len(product_array)} product(s) from Grainger PDF")
    for product in product_array:
        # determine if it is a grainger or dropship
        if not ("grainger" in product[-1].lower()): # it is a dropship
            print("grainger isn't in the address, tis a dropship")

            if product[3] in stock_product_numbers:
                print("It is a stock product")
                stock(product)
                if not product[8] == "iStock":
                    print(product[8])
                    product[8] = "iStock"
                stock_list += product
            dropship(product, grainger_pdf)
             
        else: # it is a grainger
            print("it was an grainger dammit")
    
    return product_array
