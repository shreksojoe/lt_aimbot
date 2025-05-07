import json
import sys

# open json file as an argument
# convert json file to list
# convert list elements to a smaller list
# scan the key
# action with value

if len(sys.argv) < 2:
    print("Usage python json_map.py <json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, "r") as file:
    data = json.load(file)
    
    if isinstance(data, obj):
        for key, value in data.items():
            print(f"key: {key}")
            print(f"key: {value['name']}")

    else:
        print("that sucks")
