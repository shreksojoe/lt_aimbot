import sys
sys.path.insert(0, r'c:\Users\joseph.stadum\lt_aimbot\pdf_to_csv')
import csv_sort

# Test with one of the actual CSV files
test_file = r'c:\Users\joseph.stadum\lt_aimbot\pdf_examples\4647404829.csv'
print(f"Testing csv_sort.process_file() with: {test_file}\n")

try:
    result = csv_sort.process_file(test_file)
    print(f"SUCCESS! Found {len(result)} product(s)\n")
    
    if result:
        print("First product:")
        print(f"  Vendor: {result[0][0]}")
        print(f"  PO Number: {result[0][1]}")
        print(f"  Line Number: {result[0][2]}")
        print(f"  Product Number: {result[0][3]}")
        print(f"  Description: {result[0][4]}")
        print(f"  Ship Date: {result[0][5]}")
        print(f"  Quantity: {result[0][6]}")
        print(f"  Price: {result[0][7]}")
        print(f"  Ticket Type: {result[0][8]}")
        print(f"  Address: {result[0][9][:50]}...")
        
        print("\n\nFull product array:")
        for i, product in enumerate(result):
            print(f"  Product {i+1}: {product}")
    else:
        print("No products found!")
        
    # Check if output.csv was created
    import os
    if os.path.exists('output.csv'):
        print("\nOUTPUT.CSV was created!")
        with open('output.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"  Contains {len(lines)} line(s) (including header)")
            if len(lines) > 0:
                print(f"  Header: {lines[0].strip()}")
            if len(lines) > 1:
                print(f"  First data row: {lines[1].strip()}")
    else:
        print("\nERROR: output.csv was NOT created")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
