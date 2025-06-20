import pandas as pd
import os
import sys
import csv

def convert(xlsx_file):
    # load file
    try:
        # Try with default engine
        load_file = pd.read_excel(xlsx_file)
    except ValueError:
        # If format can't be determined, try with openpyxl engine
        try:
            load_file = pd.read_excel(xlsx_file, engine='openpyxl')
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None
    
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
        else:
            new_row[7] = False
        new_array.append(new_row)
    print(f"first row: {new_array[0]}")
    print(f"first row: {new_array[1]}")
    new_array.pop(0)
    new_array.pop(0)
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

def main(input_xlsx):
    try:
        csv_file = convert(input_xlsx)
        if csv_file:
            csv_rows_to_array(csv_file)
            return csv_file
        else:
            print(f"Failed to convert {input_xlsx}")
            return input_xlsx
    except Exception as e:
        print(f"Error in xlsx_to_csv.main: {e}")
        return input_xlsx

# g 7 6 0 1 e g 9
# 0 1 2 3 4 5 6 7
