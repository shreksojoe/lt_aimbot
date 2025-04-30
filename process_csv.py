from ui import file_dup, process_csv, browse_file
from json_gps import read_json
from datetime import datetime, timedelta
import csv
import json
import time
import sys

    

tmp_path = file_dup("C:/Users/Joseph.Stadum/lt_aimbot/ticket.json")
csv_array = []

def csv_to_array(file_path):
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_array.append(row)
    return csv_array


def update_ship_date():
    date_obj = datetime.strptime(po_array[0][2], '%m/%d/%Y')
    new_date = date_obj - timedelta(weeks=2)
    return(new_date.strftime('%m/%d/%Y'))

def sort_keys ():
    with open (tmp_path, 'r') as file:
        data = json.load(file)
        keys = []
        for item in data:
            first_key = next(iter(item))
            if first_key == "Customer Name":
                item[first_key] = po_array[0][0]
            elif first_key == "PO Number":
                item[first_key] = po_array[0][1]
            elif first_key == "Ship Date":
                item[first_key] = update_ship_date()
            elif first_key == "Quantity":
                item[first_key] = po_array[0][3]
            elif first_key == "Product Number":
                item[first_key] = po_array[0][4]
            elif first_key == "Price":
                item[first_key] = po_array[0][5]
            elif first_key == "Order Notes":
                item[first_key] = po_array[0][7]
            elif first_key == "Input":
                item[first_key] = "test"
    with open (tmp_path, 'w') as file:
        json.dump(data, file, indent=4)

def print_file(file_path):
    with open (file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            print(item)

if len(sys.argv) > 1:
    arg = sys.argv[1]
    po_array = csv_to_array(arg)

sort_keys()
                
print_file(tmp_path)





