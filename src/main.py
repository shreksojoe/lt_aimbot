import ui
import os
import login
import open_files
import json_gps
# import navigation
# import csv_to_json
import csv_no_plus
import xlsx_to_csv
import auto_update
import grainger

# list of new breed (muthafuckin) files
# 1. god.py
# 2. open_files.py
# 3. navigation.py
# 4. login.py
# 5. ui.py

from utils import resource_path

# auto update
# auto_update.auto_update()

ticket_json = resource_path('instructions/ticket.json')
print(f"[DEBUG] main.py: ticket_json path: {ticket_json}")
checkbox_json = resource_path('instructions/checkboxes.json')
print(f"[DEBUG] main.py: checkbox_json path: {checkbox_json}")
order_json = resource_path('instructions/order.json')
print(f"[DEBUG] main.py: order_json path: {order_json}")
dup_order_json = resource_path('instructions/dup_order.json')
print(f"[DEBUG] main.py: dup_order_json path: {dup_order_json}")
finish_him_json = resource_path('instructions/finish_him.json')
print(f"[DEBUG] main.py: finish_him_json path: {finish_him_json}")
duplicate_json = resource_path('instructions/duplicate.json')
print(f"[DEBUG] main.py: duplicate_json path: {duplicate_json}")
relapse_json = resource_path('instructions/relapse.json')
print(f"[DEBUG] main.py: relapse_json path: {relapse_json}")

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
    if csv_file.lower().endswith(".xlsx") and 'fba' in csv_file.lower():
        print('is an xlsx')
        if csv_file.lower().endswith(".xlsx"):
            print('going into xlsx_to_csv')
            new_csv_file = xlsx_to_csv.main(csv_file)
        print(f'new csv file: {new_csv_file}')
        csv_no_plus.launch_instructions(new_csv_file, ticket_array, checkbox_array, order_array, dup_order_array, finish_him_array, duplicate_array, relapse_array)
    elif csv_file.lower().endswith(".pdf") and 'grainger' in csv_file.lower():
        grainger.execute_grainger(csv_file)
    else:
        print('is a csv')
        #  new_csv = xlsx_to_csv.main(csv_file)
        csv_no_plus.launch_instructions(csv_file, ticket_array, checkbox_array, order_array, dup_order_array, finish_him_array, duplicate_array, relapse_array)

# Keep console window open
print('\nPress Enter to exit...')
input()
