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

# gap: 40px



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


def exec_json(json_data, ops):
    for entry in json_data:
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

def type_address(address):
    for segment in address:
        data.write(segment)
        time.sleep(1)
        keyboard.press_and_release("tab")
        time.sleep(1)

def custom(product, grainger_pdf):

    product[6] = str(int(product[6]) + 30)

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

    addr = {
            "Coordinate":motion.move_rel,
            "Coordinate Maybe":motion.move_rel,
            "Window":window.title_contains,
            "Window Maybe":window.title_contains_option,
            "File Name": lambda: data.write(data.swap_slash(grainger_pdf)),
            "Address": lambda: type_address(address_array)
            }

    # Declare variables (json data) 
    cust_drop_one_data = data.load_file(data.find_rel_path("instructions\\cust_drop_one.json"))
    cust_drop_two_data = data.load_file(data.find_rel_path("instructions\\cust_drop_two.json"))
    cust_drop_three_data = data.load_file(data.find_rel_path("instructions\\cust_drop_three.json"))
    cust_drop_four_data = data.load_file(data.find_rel_path("instructiotns\\cust_drop_four.json"))
    grainger_address_data = data.load_file(data.find_rel_path("instructions\\grainger_address.json"))
    
    # Execute instructions
    exec_json(cust_drop_one_data, ops)
    if int(product[6]) < 30:
        exec_json(cust_drop_two_data, ops)
    else: exec_json(cust_drop_three_data, ops)
    exec_json(cust_drop_four_data, ops)

    data.address_search("Grainger Dropship Acct")
    address_array = data.split_addr(product[9])
    exec_json(grainger_address_data, addr)

def multiple_order(products):
    print("I sware")
    istock_two_data = data.load_file(data.find_rel_path("instructions\\istock_two.json"))

    prod = {
            "Coordinate":motion.move_rel,
            "Coordinate Maybe":motion.move_rel,
            "Window":window.title_contains,
            "Window Maybe":window.title_contains_option,
            "Product Ammount": lambda: print("filler"),
            "Quantity": lambda: data.write(product[6]),
            "Tab": lambda: keyboard.press_and_release("tab"),
            "Product No.": lambda: data.write(product[3])
            }
            
    for product in products:
        exec_json(istock_one_data, prod)
        for _ in range(3):
            time.sleep(1)
            keyboard.press_and_release("tab")
            time.sleep(1)


def stock(stock_list):
    print("stock_list: ", stock_list)
    print("Stock being executed")
    if not stock_list: return False

    istock_one_data = data.load_file(data.find_rel_path("instructions\\istock_one.json"))
    istock_two_data = data.load_file(data.find_rel_path("instructions\\istock_two.json"))

    # if len(stock_list) > 1: multiple_prod(stock_list)
    print("RUnning through it")
    for stock_product in stock_list:
        print("STOCK PRODUCT: ", stock_product)

        addr = {
                "Coordinate":motion.move_rel,
                "Coordinate Maybe":motion.move_rel,
                "Window":window.title_contains,
                "Window Maybe":window.title_contains_option,
                "File Name": lambda: data.write(data.swap_slash(grainger_pdf)),
                "Address": lambda: type_address(address_array),
                "Customer Name": lambda: data.write("W.W. Grainger"),
                "PO Number": lambda: data.write(stock_product[1]),
                "Select All":lambda: motion.select_all,
                "Ship Date": lambda: data.write(stock_product[5]),
                "Quantity": lambda: data.write(stock_product[6]),
                "Product No.": lambda: data.write(stock_product[3]),
                "Price": lambda: data.write(stock_product[7])
                }
    
        exec_json(istock_one_data, addr)
    
    # multiple_order(stock_list)

def dropship(product, grainger_pdf):
    print("Dealing with a dropship")

    if product[3] in stock_product_numbers:
        print("It is a stock product")
        # stock(product)
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
    print(f"Product Array: {product_array}")
    for product in product_array:
        # determine if it is a grainger or dropship
        # if not ("grainger" in product[-1].lower()): # it is a dropship
        print("grainger isn't in the address, tis a dropship")

        if product[3] in stock_product_numbers:
            print("It is a stock product")
            # stock(product)
            if not product[8] == "iStock":
                print(product[8])
                product[8] = "iStock"
            stock_list.append(product)
        print("stock_list: ", stock_list)
        stock(stock_list)
        dropship(product, grainger_pdf)

         
        # else: # it is a grainger
        #     print("it was an grainger dammit")
    
    return product_array
