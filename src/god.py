import ui
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
# 6. 


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

ticket_json = resource_path('instructions/ticket.json')
order_json = resource_path('instructions/order.json')
finish_him_json = resource_path('instructions/finish_him.json')

login.to_Label_Traxx()
csv_file = ui.create_window()

print('ui done, json next')

ticket_array = open_files.open_json_file(ticket_json)
order_array = open_files.open_json_file(order_json)
finish_him_array = open_files.open_json_file(finish_him_json)

csv_to_json.launch_instructions(csv_file, ticket_array, order_array, finish_him_array)

# Keep console window open
print('\nPress Enter to exit...')
input()
