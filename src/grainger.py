import window
import motion
import data
import importlib.util
import csv
import sys
import os

process_name = "Label Traxx Client.exe"
process_path = "C:\Program Files\LT Client\Label Traxx Client.exe"
lt_hwnd = window.get_hwnd(process_name)

def stock(product):
    print("tis stock: ", product)

def custom(product):

    print("tis custom: ", product)
    ops = {
            "Coordinate":motion.move_rel,
            "Window":window.title_contains,
            "Customer Name": lambda: keyboard.write("W.W. Grainger"),
            "PO Number": lambda: keyboard.write(""),
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

    # clicking actions, type:
    # Customer Name -> product[0]  "W.W. Grainger, Inc."
    # PO# -> product[1]
    # Ship Date -> product[4]
    # QTY -> product[5]
    # Product # -> product[2]
    # 
    # 
    # 
    # copy price of product 
    # 

def dropship(product):
    print("Dealing with a dropship")

    stock_product_numbers = [
    "10Y376","8X606","10Y373","8EE38","8E085", "10Y374", "8EEP0", "10Y370", "8E984", "9WA32", "10Y372", "8EE37", "10Y371", "8NCA9", "8AY66", "9WC95", "10Y495"
    ]
    
    if product[2] in stock_product_numbers:
        print("It is a stock product")
        stock(product)
        if not product[7] == "iStock":
            print(product[7])
            product[7] = "iStock"
        print(product[7])
    else:
        print("this is a custom product")
        print(product[7])

        if not product[7] == "Custom":
            print(product[7])
            product[7] = "Custom"
        print(product[7])

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
    for product in product_array:
        print(product)
        # determine if it is a grainger or dropship
        if not ("grainger" in product[-1].lower()): # it is a dropship
            print("grainger isn't in the address, tis a dropship")
            dropship(product)
        else: # it is a grainger
            print("it was an grainger dammit")
    
    return product_array
