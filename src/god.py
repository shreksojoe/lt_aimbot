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



ticket_json = 'instructions\\ticket.json'
order_json = 'instructions\\order.json'

login.to_Label_Traxx()
csv_file = ui.create_window()

print('ui done, json next')

ticket_array = open_files.open_json_file(ticket_json)
order_array = open_files.open_json_file(order_json)

csv_to_json.launch_instructions(csv_file, ticket_array, order_array)
