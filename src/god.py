import ui
import login
import open_files
import json_gps
import navigation
import csv_to_json

# list of new breed (muthafuckin) files
# 1. god.py
# 2. open_files.py
# 3. navigation.py
# 



json_file = 'instructions\\ticket.json'

login.to_Label_Traxx()
csv_file = ui.create_window()

print('ui done, json next')

json_array = open_files.open_json_file(json_file)
print(json_array)
print('open_files is done, moving onto csv_to_json')

csv_to_json.csv_into_json(csv_file, json_array)
