import json
import csv

# Open csv file :D
def open_csv_file(ticket):
    with open(ticket, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)  # each row is a list of strings

# Open json file and return array of key-value pairs
def open_json_file(manual):
    """
    Read a JSON file and return an array of key-value pairs.
    Handles the specific structure of ticket.json where each item is a dictionary
    with a single key-value pair.
    """
    with open(manual, 'r') as f:
        data = json.load(f)
    
    result = []
    for item in data:
        # Create a new dictionary for each item, excluding the 'Name' key
        filtered_item = {k: v for k, v in item.items() if k != 'Name'}
        if filtered_item:  # Only add if there are items after filtering
            result.append(filtered_item)
    
    return result
