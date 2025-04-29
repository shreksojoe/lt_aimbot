from ui import file_dup, process_csv, browse_file
from json_gps import read_json

tmp_path = file_dup("C:/Users/Joseph.Stadum/lt_aimbot/ticket.json")

def csv_to_array(file_path):
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_array.append(row)
    return csv_array

po_array = csv_to_array(browse_file())

def update_ship_date():
    return po_array[2]

def sort_keys ():
    with open (tmp_path, 'r') as file:
        data = json.load(file)
        keys = []
        for item in data
            first_key = next(iter(item))
            if first_key == "Customer Name":
                item[first_key] = po_array[0]
            elif first_key == "PO Number":
                item[first_key] = po_array[1]
            elif first_key == "Ship Date":
                item[first_key] = update_ship_date()
            elif first_key == "Quantity":
                item[first_key] = po_array[3]
            elif first_key == "Product Number":
                item[first_key] = po_array[4]
            elif first_key == "Price":
                item[first_key] = po_array[5]
            elif first_key == "Order Notes":
                item[first_key] = po_array[7]
            elif first_key == "Input":
                





