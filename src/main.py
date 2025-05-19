# also the order at which everything runs:

import ui
import login
import process_csv
import json_gps
import address_search

login.to_Label_Traxx() #launch Label traxx and navigate to starting point
temp_file = ui.create_window() #select csv, and open ui
json_file = process_csv.start(temp_file)
json_gps(json_file)

