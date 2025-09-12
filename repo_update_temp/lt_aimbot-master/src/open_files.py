import json
import csv

# Open csv file :D
def open_csv_file(ticket):
    # List of encodings to try
    encodings = ['utf-8', 'latin1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(ticket, newline='', encoding=encoding) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    print(row)  # each row is a list of strings
            # If we get here, the file was read successfully
            break
        except UnicodeDecodeError:
            # If this encoding didn't work, try the next one
            if encoding == encodings[-1]:
                # If we've tried all encodings, raise the error
                print(f"Failed to read {ticket} with any of the attempted encodings")
                raise

# Open json file and return array of key-value pairs
from utils import resource_path

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
    # Always resolve the path relative to the install location, not the working directory
    manual_path = resource_path(manual)
    print(f"[DEBUG] open_json_file is trying to open: {manual_path}")
    with open(manual_path, 'r') as f:
        data = json.load(f)

    result = []
    for item in data:
        # For each key-value pair in the object, create a separate dictionary
        for key, value in item.items():
            result.append({key: value})

    return result
