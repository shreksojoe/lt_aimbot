from ui import file_dup, process_csv, browse_file
# from json_gps import read_json
from datetime import datetime, timedelta
import csv
import json
import time
import sys
import subprocess

    
tmp_path = file_dup("C:/Users/Joseph.Stadum/lt_aimbot/ticket.json")
csv_array = []


# turn csv to an array
def csv_to_array(file_path):
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_array.append(row)
    return csv_array

# set ship date to 2 weeks prior
def update_ship_date():
    try: 
        date_obj = datetime.strptime(po_array[0][2], '%m/%d/%Y')
        new_date = date_obj - timedelta(weeks=2)
        return(new_date.strftime('%m/%d/%Y'))
    except ValueError:
        date_obj = datetime.strptime(po_array[0][2], '%m/%d/%y')
        new_date = date_obj - timedelta(weeks=2)
        return(new_date.strftime('%m/%d/%y'))

# add csv values to json
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

# print json files
def print_file(file_path):
    with open (file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            print(item)

if len(sys.argv) > 1:
    arg2 = sys.argv[1]
    po_array = csv_to_array(arg2)
 
sort_keys()
                
print_file(tmp_path)

json_gps = 'json_gps.py'
subprocess.run(["python", json_gps, tmp_path])




