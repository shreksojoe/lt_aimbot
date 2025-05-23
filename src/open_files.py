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
    Read a JSON file containing a list of objects and return a list of key-value pairs.
    Each object in the input JSON will be flattened into key-value pairs.
    
    Example input JSON:
    [
        {"name": "John", "age": 30},
        {"city": "New York", "country": "USA"}
    ]
    
    Example output:
    [{"name": "John"}, {"age": 30}, {"city": "New York"}, {"country": "USA"}]
    """
    with open(manual, 'r') as f:
        data = json.load(f)
    
    result = []
    for item in data:
        # For each key-value pair in the object, create a separate dictionary
        for key, value in item.items():
            result.append({key: value})
    
    return result
