import ui
import os
import login
import open_files
import json_gps
# import navigation
import csv_to_json

# list of new breed (muthafuckin) files
# 1. god.py
# 2. open_files.py
# 3. navigation.py
# 4. login.py
# 5. ui.py

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

ticket_json = resource_path('instructions/ticket.json')
checkbox_json = resource_path('instructions/checkboxes.json')
order_json = resource_path('instructions/order.json')
finish_him_json = resource_path('instructions/finish_him.json')
relapse_json = resource_path('instructions/relapse.json')

login.to_Label_Traxx()
csv_files = ui.create_window()

print('ui done, json next')

ticket_array = open_files.open_json_file(ticket_json)
checkbox_array = open_files.open_json_file(checkbox_json)
order_array = open_files.open_json_file(order_json)
finish_him_array = open_files.open_json_file(finish_him_json)
relapse_array = open_files.open_json_file(relapse_json)

for csv_file in csv_files:
    csv_to_json.launch_instructions(csv_file, ticket_array, checkbox_array, order_array, finish_him_array, relapse_array)

# Keep console window open
print('\nPress Enter to exit...')
input()
