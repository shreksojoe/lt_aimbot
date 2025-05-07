import csv
import sys
import json
import re


def zip_extractor(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        zips = re.findall(r'\b\d{5}(?:-\d{4})?\b', file_contents)
        if len(zips) >=2:
            return zips[1]
        elif len(zips) == 1:
            return zips[0]
        else:
            return None
    


if len(sys.argv) > 1:
    print("Usage: python csv_to_string.py <file.csv>")
    filename = sys.argv[1]
    output = zip_extractor(filename)  
    print(output)
    sys.exit(1)
    
    
