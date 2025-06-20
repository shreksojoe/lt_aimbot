import os
import sys

# Fix for pandas/numpy import in PyInstaller
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    
    # Add bundle directory to path to help find pandas/numpy
    if bundle_dir not in sys.path:
        sys.path.insert(0, bundle_dir)

# Now import the rest of the modules
import ui
import login
import open_files
import json_gps
# import navigation
import csv_to_json
import xlsx_to_csv

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

ticket_json = resource_path('instructions/ticket.json')
checkbox_json = resource_path('instructions/checkboxes.json')
order_json = resource_path('instructions/order.json')
dup_order_json = resource_path('instructions/dup_order.json')
finish_him_json = resource_path('instructions/finish_him.json')
duplicate_json = resource_path('instructions/duplicate.json')
relapse_json = resource_path('instructions/relapse.json')

login.to_Label_Traxx()
csv_files = ui.create_window()

print('ui done, json next')

ticket_array = open_files.open_json_file(ticket_json)
checkbox_array = open_files.open_json_file(checkbox_json)
order_array = open_files.open_json_file(order_json)
dup_order_array = open_files.open_json_file(dup_order_json)
finish_him_array = open_files.open_json_file(finish_him_json)
duplicate_array = open_files.open_json_file(duplicate_json)
relapse_array = open_files.open_json_file(relapse_json)

for csv_file in csv_files:
    if csv_file.lower().endswith(".xlsx"):
        print('is an xlsx')
        new_csv = xlsx_to_csv.main(csv_file)
        csv_to_json.launch_instructions(new_csv, ticket_array, checkbox_array, order_array, dup_order_array, finish_him_array, duplicate_array, relapse_array, True)
    else:
        print('is a csv')
        #  new_csv = xlsx_to_csv.main(csv_file)
        csv_to_json.launch_instructions(csv_file, ticket_array, checkbox_array, order_array, dup_order_array, finish_him_array, duplicate_array, relapse_array, False)

# Keep console window open
print('\nPress Enter to exit...')
input()
