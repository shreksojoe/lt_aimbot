import json
import csv
import sys
import os

csv_rows = []

def csv_into_json(user_csv, user_json):

    with open(user_csv, newline = '') as opened_csv:
        reader = csv.reader(opened_csv)
        for row in reader:
            csv_rows.append(row)
        
    print(f'CSV as an array: {csv_rows}')



# Take csv and json as input

if (len(sys.argv) <= 2):
    print('Did not input enough files. Exiting ...')
    sys.exit()

if (not sys.argv[1].endswith('.csv')):
    print('First file is not a csv. Exiting ...')
    sys.exit()

if (not sys.argv[2].endswith('.json')):
    print('Second file is not a json. Exiting ...')
    sys.exit()

csv_into_json(sys.argv[1],sys.argv[2])

# We have now determined that we have a csv and json file
# We need to add the csv elements to the json file
# 1. Cycle through csv
# 2. Cycle through json
# 3. 






