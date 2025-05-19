#from ui import file_dup, process_csv, browse_file
# from json_gps import read_json
import ui
from datetime import datetime, timedelta
import csv
import json
import time
import sys
import os
import json_gps
import path_finder

    
fd_path = path_finder.find_rel_path("src", "instructions/ticket.json")
csv_array = []

# duplicates file
def file_dup(path):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    temp_path = temp_file.name
    temp_file.close()

    shutil.copy2(str(path), str(temp_path))
    return temp_path

tmp_path = ui.file_dup(fd_path)

# turn csv to an array
def csv_to_array(file_path):
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_array.append(row)
    return csv_array

# set ship date to 2 weeks prior
def update_ship_date(input_date):
    try: 
        input_date = datetime.strptime(date_str, "%m/%d/%Y")
        new_date = input_date - timedelta(weeks=2)
        return new_date.strftime("%m/%d/%Y")
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
                item[first_key] = update_ship_date(po_array[0][2])
            elif first_key == "Quantity":
                item[first_key] = po_array[0][3]
            elif first_key == "Product Number":
                item[first_key] = po_array[0][4]
            elif first_key == "Price":
                item[first_key] = po_array[0][5]
            elif first_key == "Order Notes":
                try:
                    item[first_key] = po_array[0][7]
                except IndexError:
                    print("No notes found.")
                    continue
            elif first_key == "Zip":
                try:
                    item[first_key] = int(po_array[0][6])
                except ValueError:
                    item[first_key] = po_array[0][6]
    with open (tmp_path, 'w') as file:
        json.dump(data, file, indent=4)

# print json files
def print_file(file_path):
    with open (file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            print(item)

def start(csv):
    global po_array
    po_array = csv_to_array(csv)
     
    sort_keys()
    
    return tmp_path

if (len(sys.argv) > 1):
    start(sys.argv[1])
else:
    print('no file inputed')



