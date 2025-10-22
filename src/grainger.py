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
import subprocess
import shutil

process_name = "Label Traxx Client.exe"
process_path = "C:\Program Files\LT Client\Label Traxx Client.exe"
lt_hwnd = window.get_hwnd(process_name)

stock_product_numbers = [
"10Y376","8X606","10Y373","8EE38","8E085", "10Y374", "8EEP0", "10Y370", "8E984", "9WA32", "10Y372", "8EE37", "10Y371", "8NCA9", "8AY66", "9WC95", "10Y495"
]

def copy():
    time.sleep(1)
    pyperclip.copy("")
    keyboard.press("ctrl")
    keyboard.press_and_release("c")
    keyboard.release("ctrl")
    clipboard = pyperclip.paste()
    print("copied: ", clipboard)
    time.sleep(1)

def ctrl_a():
    print("run ctlra  ")
    time.sleep(1)
    keyboard.press("ctrl")
    keyboard.press_and_release("a")
    keyboard.release("ctrl")
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

def strip_zeros_refined(text, handle_2d=False, index=2, desc_index=4):

    # --- Handle 2D array case ---
    if handle_2d:
        if not (isinstance(text, list) and all(isinstance(row, list) for row in text)):
            raise TypeError("For 2D handling, 'text' must be a list of lists.")

        nums = []
        descs = []
        for row in text:
            try:
                val = row[index].strip()
                desc = row[desc_index].strip()
                nums.append(val)
                descs.append(desc)
            except IndexError:
                print(f"Warning: row {row} missing required index, skipping.")
                continue

        # Strip zeros from numbers
        stripped = [str(int(num)) for num in nums if num.isdigit()]
        joined = ",".join(stripped)
        string = f"L#{joined} - "

        # Find common text among all descriptions
        if len(descs) > 1:
            common_prefix = _longest_common_substring(descs)
        else:
            common_prefix = descs[0] if descs else ""

        # --- Remove commas from description only ---
        common_prefix = common_prefix.replace(",", " ")

    # --- Handle string or list of strings ---
    else:
        if isinstance(text, str):
            nums = [t.strip() for t in text.split(",") if t.strip()]
        elif isinstance(text, list):
            nums = [t.strip() for t in text if isinstance(t, str) and t.strip()]
        else:
            raise TypeError("Input must be a string, list of strings, or 2D list (with handle_2d=True).")

        stripped = [str(int(num)) for num in nums if num.isdigit()]
        joined = ",".join(stripped)
        string = f"L#{joined} - "
        common_prefix = ""

    # --- Get clipboard text ---
    clip = pyperclip.paste()
    print("Clipboard contents:", clip)

    # Combine everything
    gen_desc = string + common_prefix
    print("General description:", gen_desc)

    if 'data' in globals():
        data.write("TEST")
        print(f"lord farqwad {gen_desc}")
        # change this when testing is done
        # data.write(gen_desc)
    else:
        print("Warning: 'data' file handle not found. Skipping write.")

    return gen_desc


def _longest_common_substring(strings):
    """
    Returns the longest common substring (word-based) shared by all strings in the given list.
    """
    # Split all strings into word chunks for better natural matching
    split_strings = [re.split(r'[\s,]+', s) for s in strings]
    shortest = min(split_strings, key=len)

    # Find overlap word-by-word
    common = []
    for i, word in enumerate(shortest):
        if all(i < len(s) and s[i] == word for s in split_strings):
            common.append(word)
        else:
            break

    return " ".join(common)

# we trying thi sother one^^^^^
def strip_zeros(text):
    print("desciption, no?")
    pyautogui.press('end')
    time.sleep(0.5)
    print("typing ctrl + a")
    ctrl_a()
    
    print("Passed into strip zeros: ", text)
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
 
def type_line_number(line_num):
    print(f"running type line number: {line_num}")
    ctrl_a()
    data.write(line_num)

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

def type_address(product, address=None):
    if product[10] == False:
        if not address: 
            address = product[9]
        print("Dropship")
        for segment in address:
            data.write(segment)
            time.sleep(1)
            keyboard.press_and_release("tab")
            time.sleep(1)
    else:
        print("Not a dropship, searching for default address")
        data.address_search(data.extract_zip(product[9]))

def date_determiner(product):
    if product[10] is False:
        data.write(data.move_to_wed(data.standardize_date(product[5])))
        print("Typeing dropship date")
    else:
        data.write(product[5])
        print("not a dropship")

def product_points(product, grainger_pdf, total_quantity):
    cust_drop_one_data = data.load_file(data.find_rel_path("instructions\\cust_drop_one.json"))
    cust_drop_two_data = data.load_file(data.find_rel_path("instructions\\cust_drop_two.json"))
    cust_drop_three_data = data.load_file(data.find_rel_path("instructions\\cust_drop_three.json"))
    cust_drop_four_data = data.load_file(data.find_rel_path("instructions\\cust_drop_four.json"))
    grainger_address_data = data.load_file(data.find_rel_path("instructions\\grainger_address.json"))

    ops = {
            "Coordinate":motion.move_rel,
            "Coordinate Maybe":motion.move_rel,
            "Window":window.title_contains,
            "Window Maybe":window.title_contains_option,
            "Customer Name": lambda: data.write("W.W. Grainger"),
            "PO Number": lambda: data.write(product[1]),
            "Select All": motion.select_all,
            "Ship Date": lambda: date_determiner(product),
            "Low Stock": lambda: data.write("test"),
            "Quantity": lambda: data.write(product[6]),
            "Product No.": lambda: data.write(product[3]),
            "Price": lambda: data.compare(product[7]),
            "Copy": copy,
            "Line Number": lambda: strip_zeros(product[2]),
            "Line Number Zero": lambda: type_line_number(product[2]),
            "Move Down": lambda: move_down(2),
            "Click": lambda: pyautogui.click()
            }


    addr = {
            "Coordinate":motion.move_rel,
            "Coordinate Maybe":motion.move_rel,
            "Window":window.title_contains,
            "Window Maybe":window.title_contains_option,
            "File Name": lambda: data.write(data.swap_slash(grainger_pdf)),
            "Address": lambda: type_address(product, address_array)
            }

    exec_json(cust_drop_one_data, ops)
    print(f"total quantity: {total_quantity}")
    if total_quantity > 30:
        exec_json(cust_drop_two_data, ops)
    else: exec_json(cust_drop_three_data, ops)

    exec_json(cust_drop_four_data, ops)

    if not "grainger" in product[9].lower():
        data.address_search("Grainger Dropship Acct")
        address_array = product[9].splitlines()
        address_array[0] = ' '.join([address_array[0], address_array[1]])
        del address_array[1]
        print(f"address array: {address_array}")
        exec_json(grainger_address_data, addr)
    else:



def custom(custom_list, grainger_pdf, total_quantity):

    
    ops = {
            "Coordinate":motion.move_rel,
            "Coordinate Maybe":motion.move_rel,
            "Window":window.title_contains,
            "Window Maybe":window.title_contains_option,
            "Customer Name": lambda: data.write("W.W. Grainger"),
            "PO Number": lambda: data.write(product[1]),
            "Select All": motion.select_all,
            "Ship Date": lambda: date_determiner(product),
            "Low Stock": lambda: data.write("test"),
            "Quantity": lambda: data.write(product[6]),
            "Product No.": lambda: data.write(product[3]),
            "Price": lambda: data.compare(product[7]),
            "Copy": copy,
            "Line Number": lambda: strip_zeros(product[2]),
            #fucking help me
            "Line Number Zero": lambda: type_line_number(product[2]),
            "Move Down": lambda: move_down(2),
            "Click": lambda: pyautogui.click()
            }

    print("tis custom: ", custom_list)

    cust_drop_dup_data = data.load_file(data.find_rel_path("instructions\\cust_drop_dup.json"))

    product_points(custom_list[0], grainger_pdf, total_quantity)

    for product in custom_list[1:]:
        time.sleep(0.4)
        motion.move_rel(lt_hwnd, 911, 273)
        time.sleep(0.4)
        motion.move_rel(lt_hwnd, 339, 251)
        time.sleep(0.2)
        motion.move_rel(lt_hwnd, 638, 510)
        time.sleep(0.2)
        exec_json(cust_drop_dup_data, ops)
    motion.move_rel(lt_hwnd, 925, 188)
    motion.move_rel(lt_hwnd, 905, 641)



def multiple_stock(products):
    print("I sware")
    istock_two_data = data.load_file(data.find_rel_path("instructions\\istock_two.json"))
    istock_setup_data = data.load_file(data.find_rel_path("instructions\\istock_setup.json"))

    prod = {
            "Coordinate":motion.move_rel,
            "Coordinate Maybe":motion.move_rel,
            "Window":window.title_contains,
            "Window Maybe":window.title_contains_option,
            "Product Ammount": lambda: data.write(str(len(products) - 1)),
            "Quantity": lambda: data.write(product[6]),
            "Tab": lambda: keyboard.press_and_release("tab"),
            "Product No.": lambda: data.write(product[3]),
            "Price": lambda: data.write(product[7])
            }
            
    exec_json(istock_setup_data, prod)
    for product in products:
        exec_json(istock_two_data, prod)
        for _ in range(2):
            time.sleep(1)
            keyboard.press_and_release("tab")
            time.sleep(1)


def stock(stock_list, grainger_pdf):
    print("stock_list: ", stock_list)
    print("Stock being executed")
    if not stock_list: return False

    istock_one_data = data.load_file(data.find_rel_path("instructions\\istock_one.json"))
    istock_two_data = data.load_file(data.find_rel_path("instructions\\istock_two.json"))
    istock_three_data = data.load_file(data.find_rel_path("instructions\\istock_three.json"))
    grainger_address_data = data.load_file(data.find_rel_path("instructions\\grainger_address.json"))

    # if len(stock_list) > 1: multiple_prod(stock_list)
    print("RUnning through it")
    stock_product = stock_list[0]
    print("STOCK PRODUCT: ", stock_product)

    addr = {
            "Coordinate":motion.move_rel,
            "Coordinate Maybe":motion.move_rel,
            "Window":window.title_contains,
            "Window Maybe":window.title_contains_option,
            "File Name": lambda: data.write(data.swap_slash(grainger_pdf)),
            "Address": lambda: print("Address filler"),
            "Customer Name": lambda: data.write("W.W. Grainger"),
            "PO Number": lambda: data.write(stock_product[1]),
            "Select All": motion.select_all,
            "Ship Date": lambda: date_determiner(stock_product),
            "Quantity": lambda: data.write(stock_product[6]),
            "Product No.": lambda: data.write(stock_product[3]),
            "Price": lambda: data.write(stock_product[7]),
            "Ctrl a": ctrl_a,
            "Copy": copy,
            "Paste": lambda: strip_zeros_refined(stock_list, True),
            "Tab": lambda: keyboard.press_and_release("tab")
            }

    exec_json(istock_one_data, addr)
    
    multiple_stock(stock_list)
    exec_json(istock_three_data, addr)
    print("Search for: ", stock_list[0][9])
    type_address(stock_list[0])
    exec_json(grainger_address_data, addr)
    motion.move_rel(lt_hwnd, 925, 188)
    motion.move_rel(lt_hwnd, 905, 641)
    pyautogui.click()

def execute_grainger(grainger_pdf):
    # TXT file path
    txt_file = r"c:\Users\joseph.stadum\lt_aimbot\server_csv\text_data\\" + os.path.splitext(os.path.basename(grainger_pdf))[0] + ".txt"
    
    # Run llama_trainer.py to convert PDF to TXT
    subprocess.run(["python", r"c:\Users\joseph.stadum\lt_aimbot\server_csv\llama_trainer.py", grainger_pdf, txt_file])
    
    # Run txt_to_csv.py on the TXT to produce CSV
    final_csv_dir = r"c:\Users\joseph.stadum\lt_aimbot\server_csv\final_csv"
    os.makedirs(final_csv_dir, exist_ok=True)
    subprocess.run(["python", r"c:\Users\joseph.stadum\lt_aimbot\server_csv\txt_to_csv.py", txt_file, "--out", final_csv_dir])
    
    # CSV file path
    csv_file = r"c:\Users\joseph.stadum\lt_aimbot\server_csv\final_csv\\" + os.path.splitext(os.path.basename(grainger_pdf))[0] + ".csv"
    
    # Load CSV into product_array
    product_array = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            product_array.append(row)
    
    print(f"Processed {len(product_array)} product(s) from Grainger PDF")
    print(f"Product Array: {product_array}")
    
    stock_list = []
    custom_list = []
    
    # First pass: categorize all products
    for product in product_array:
        # determine if it is a grainger or dropship
        if not ("grainger" in product[9].lower()): # it is a dropship
            product.append(False)
            # move date to next wednesday
            print(f"Product {product[2]} is a dropship")
        else:
            product.append(True)
            print(f"Product {product[2]} is grainger")

        if product[3] in stock_product_numbers:
            print(f"Product {product[2]} ({product[3]}) is a stock product")
            # Ensure ticket type is iStock
            if not product[8] == "iStock":
                product[8] = "iStock"
            stock_list.append(product)
        else:
            print(f"Product {product[2]} ({product[3]}) is a custom product")
            custom_list.append(product)
    
    # Second pass: process each category once
    print(f"\nFinal stock_list ({len(stock_list)} products): {stock_list}")
    print(f"Final custom_list ({len(custom_list)} products): {custom_list}")
    
    total_quantity = sum((int(row[6]) for row in product_array))
    print(f"lalala total quantity: {total_quantity}")

    if stock_list: 
        print(f"Executing stocklist: {stock_list}")
        stock(stock_list, grainger_pdf)
    if custom_list:
        print(f"Executing custom list: {custom_list}")
        custom(custom_list, grainger_pdf, total_quantity)
    
    return product_array
