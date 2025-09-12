import pandas as pd
import os
import sys
import csv

# issue is this returning a NoneType
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
    print(f'Processing {len(file_array)} rows')

    for row in file_array:
        # Convert first cell to string and strip whitespace
        first_cell = str(row[0]).strip() if row and len(row) > 0 and row[0] is not None else ''
        
        # Only keep rows where first cell is a positive integer
        if first_cell.isdigit() and int(first_cell) > 0:
            try:
                new_row = [None] * 8
                new_row[0] = 'Chromalabel'  # Fixed value
                new_row[3] = first_cell  # QTY (already validated as positive integer)
                new_row[4] = str(row[1]) if len(row) > 1 and row[1] is not None else ''  # SKU
                new_row[5] = ''  # Empty column
                new_row[2] = str(row[6]) if len(row) > 6 and row[6] is not None else ''  # ENTERED date
                new_row[1] = str(row[7]) if len(row) > 7 and row[7] is not None else ''  # PO Number
                new_row[6] = 'AMAZON FBA USA'  # Fixed value
                # Check stock status safely
                stock_status = str(row[9]).lower() if len(row) > 9 and row[9] is not None else ''
                new_row[7] = 'low stock' in stock_status or 'out of stock' in stock_status
                
                new_array.append(new_row)
                
            except Exception as e:
                print(f'Skipping row due to error: {e}')
                continue

    print(f'Processed {len(new_array)} valid rows')
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
        # convert xlsx file to a csv
        csv_file = convert(input_xlsx)
        print(f'csv_file is a: {type(csv_file)}')

        # if csv_file.endswith('.csv'):
        #    print('successfuly converted to a csv')

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
