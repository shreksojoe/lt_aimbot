import pandas as pd
import os
import sys
import csv

def convert(xlsx_file):
    # load file
    load_file = pd.read_excel(xlsx_file)
    
    # declare and assign the name of the csv file
    base_name = os.path.splitext(xlsx_file)[0]
    csv_file = f"{base_name}.csv"
    
    # takes the open xlsx file and writes it to a csv
    load_file.to_csv(csv_file, index=False, encoding='utf-8-sig')

    return csv_file

def construct(file_array):
    new_array = []
    for i in range(0, len(file_array)):
        # Create a new list for each iteration
        new_row = [None] * 8
        new_row[0] = ('Chromalabel')
        new_row[3] = file_array[i][0]
        new_row[4] = file_array[i][1]
        new_row[5] = ''
        new_row[2] = file_array[i][6]
        new_row[1] = file_array[i][7]
        new_row[6] = 'AMAZON FBA USA'

        if ('low stock' in file_array[i][9].lower()) or ('out of stock' in file_array[i][9].lower()):
            new_row[7] = True
        elif not ('low stock' in file_array[i][9].lower()):
            new_row[7] = False
        new_array.append(new_row)
    return new_array

# Opens the csv, and stores rows in array 
def csv_rows_to_array(input_csv):
    row_array = []
    with open(input_csv, newline = '') as opened_csv:
        reader = csv.reader(opened_csv)
        for row in reader:
            row_array.append(row)
    with open(input_csv, "w", newline="") as old_file:
        new_file = construct(row_array)
        print(new_file)
        writer = csv.writer(old_file)
        writer.writerows(new_file)


xlsx_file = 'C:\\Users\\joseph.stadum\\Downloads\\FBA-US-215.xlsx'
csv_rows_to_array(convert(xlsx_file))

# g 7 6 0 1 e g 9
# 0 1 2 3 4 5 6 7

