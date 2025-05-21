# also the order at which everything runs:

import ui
import login
import process_csv
import json_gps
import address_search

# Launch Label Traxx and navigate to starting point
login.to_Label_Traxx()

# Select CSV file and open UI
temp_file = ui.create_window()

# Process the CSV file and get the JSON file path
json_file = process_csv.start(temp_file)

# Read the JSON file and process the data
if json_file:
    data = json_gps.read_json(json_file)
    if data is not None:
        print("Successfully read JSON data:", data)
        # If you need to process coordinates, uncomment the following:
        zip_code = json_gps.read_coords(data)
        print(f"Processed zip code: {zip_code}")
else:
    print("No JSON file was processed.")
