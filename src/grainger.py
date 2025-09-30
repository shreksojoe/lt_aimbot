import window
import motion
import data
import importlib.util
import csv
import sys
import os
from utils import resource_path
import open_files

# custom dropship instructions variables
cust_drop_one_json = resource_path("instructions/cust_drop_one.json")
cust_drop_one_array = open_files.open_json_file(cust_drop_one_json)


def stock(product):
    print("tis stock: ", product)

def custom(product):
    print("tis custom: ", product)

def dropship(product):
    print("Dealing with a dropship")

    stock_product_numbers = [
    "10Y376","8X606","10Y373","8EE38","8E085", "10Y374", "8EEP0", "10Y370", "8E984", "9WA32", "10Y372", "8EE37", "10Y371", "8NCA9", "8AY66", "9WC95", "10Y495"
    ]
    
    if product[2] in stock_product_numbers:
        print("It is a stock product")
        stock(product)
    else:
        print("this is a custom product")
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
            print("it was an iStock dammit")
    
    print(cust_drop_one_array)
    return product_array
