from datetime import datetime, timedelta
import csv
import sys
import re
import os

# handles data gathering for po's with more than 2 orders (for some reason 3+ changes the process)
def extract_po_data(file_path, start_row):
    # Load CSV as raw lines
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Initialize
    product_lines = []
    skip_count = 0
    i = start_row
    total_lines = len(lines)

    # Step 1: Detect initial product lines "(0000x"
    initial_products = []
    while i < total_lines:
        if skip_count > 0:
            skip_count -= 1
            i += 1
            continue
        line = lines[i]
        # Skip page breaks
        if "Page" in line and "of" in line:
            skip_count = 6
            i += 1
            continue
        if re.match(r"\(\d{5}", line):
            # Extract just the numeric part of the line number
            line_number = re.sub(r'\D', '', line)
            initial_products.append([line_number])  # store line number as first element
            i += 1
        else:
            break

    n = len(initial_products)

    # Step 2: Append next n rows one-to-one
    for j in range(n):
        if i < total_lines:
            row = re.sub(r"[\[\]\|]", "", lines[i])  # remove OCR artifacts
            initial_products[j].append(row)
            i += 1

    # Step 3: Append next line to first product line
    if i < total_lines:
        row = re.sub(r"[\[\]\|]", "", lines[i])
        initial_products[0].append(row)
        i += 1

    # Step 4: Process each product line for Qty and Date
    processed_count = 0
    while processed_count < n and i < total_lines:
        line = lines[i]
        if "Page" in line and "of" in line:
            skip_count = 6
            i += 1
            continue
        line_clean = re.sub(r"[\[\]\|]", "", line)

        # Find Qty
        if "Qty:" in line:
            qty_match = re.search(r"Qty:.*?(\d+)", line)
            if qty_match:
                initial_products[processed_count].append(qty_match.group(1))
            i += 1
            continue

        # Find Subline and Date
        if "Subline" in line and "Date:" in line:
            date_match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", line)
            if date_match:
                initial_products[processed_count].insert(-1, date_match.group(1))
            i += 1
            processed_count += 1  # move to next product line
            # Append the next row to next product line if exists
            if processed_count < n and i < total_lines:
                row = re.sub(r"[\[\]\|]", "", lines[i])
                initial_products[processed_count].append(row)
                i += 1
            continue

        i += 1

    # Step 5: Skip "Each" rows
    while i < total_lines and lines[i].startswith("Each"):
        i += 1

    # Step 6: Append prices (first numeric value) to product lines
    price_count = 0
    while price_count < n and i < total_lines:
        line = re.sub(r"[\[\]\|]", "", lines[i])
        price_match = re.search(r"\d+\.\d{2}", line)
        if price_match:
            initial_products[price_count].append(price_match.group(0))
            price_count += 1
        i += 1

    return initial_products

# product details: Grainger, po #, line number, product #, Description, ship date, Qty, price, address
# def extract_po_base(file_name, start_row):
    

# main execution, also what gathers the data for the default po (2 or less products in po
def process_file(file_name):
    with open(file_name, newline="", encoding="utf-8", errors="replace") as infile:

        reader = csv.reader(infile)
        product_details = []
        row_list = list(reader)
        Found_Po = 0 
        Found_Ticket_Type = 0
        Found_Product_Num = 0
        Found_Address = 0
        Format_Repeat = 0
        next_page = 0 
        addr = ""
        prod_arr = []
        Is_Stock = False
        Stock_Products = ["10Y376","8X606","10Y373","8EE38","8E085","10Y374","8EEP0","10Y37","8E984","9WA32","10Y372","8EE37", "10Y371", "8NCA9", "8AY66", "9WC95", "10Y495"]

        po_number = "" # got em
        ticket_type = "" # got em
        is_complicated = False
        qty_list = []  # Collect all quantities
        date_list = []  # Collect all dates
        price_list = []  # Collect all prices
        collecting_products = True  # Flag to know when we're done collecting product lines

        # Grainger, PO #, product details, Type, address
        # product details: line number, po #, Description, ship date, Qty, price
        #                  extract line number

        # Go through csv line by line
        for i, row in enumerate(row_list):

            # skip second page heading and what not
            if ("Page" in row and "of" in row) or (0 < next_page < 7):
                next_page += 1
                continue
            next_page = 0

            #  Get address
            if "Vendor:" in row and "Ship" in row and "To:" in row: # mark where to start looking for the address
                Found_Address = 1
                continue
            elif "Ship-To" in row and "Qualifier:" in row: # mark end of address
                Found_Address = 10
                continue
            elif Found_Address == 1: # add each element to the full address
                addr += ' '.join(row) # concat all elements of the address into a string
            
            # get product details
            if is_format(row[0]):
                if len(row) == 1:
                    Format_Repeat += 1
                    continue
                # other words OSR read it correctly
                else:
                    # manipulate product details so it shows only the necessary information
                    try:
                        del row[-1] # delete last cell
                        row.pop(-2)
                        row[0] = row[0] if row[0].isdigit() else re.sub(r'\D', '', row[0])
                        row[2:-1] = [' '.join(row[2:-1])]
                    except IndexError:
                        print(f'that index was out of wack. Here is the row: {row}')
                    product_details.append(row) 
                    Found_Product_Num += 1 

            elif Format_Repeat > 1: 
                start_row = i - Format_Repeat
                product_data = extract_po_data(file_name, start_row)
                product_details = product_data
                is_complicated = True
                Format_Repeat = 0
            elif not is_complicated and len(product_details) > 0:
                # Once we hit qty/date rows, we're done collecting products
                if collecting_products and ("Qty:" in row or ("Ship" in row and "Date:" in row)):
                    collecting_products = False
                
                # Collect all quantities, dates, and prices into separate lists
                if not collecting_products:
                    if "Qty:" in row:
                        qty_match = re.search(r'Qty:.*?(\d+)', ' '.join(row))
                        if qty_match:
                            qty_list.append(qty_match.group(1))
                    elif "Ship" in row and "Date:" in row: # get the ship date
                        date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', ' '.join(row))
                        if date_match:
                            date_list.append(date_match.group(1))
                    elif "Each" not in row and len(qty_list) > 0 and len(date_list) > 0:
                        # After collecting qty/date, look for prices
                        price_match = re.search(r'\d+\.\d{2}', ' '.join(row))
                        if price_match:
                            price_list.append(price_match.group(0))
            
                # cycle through cells
            for j, cell in enumerate(row):
                if cell == "Original": # detect if PO number is on the next line
                    Found_Po += 1 
                elif Found_Po == 1: 
                    po_number = cell
                    Found_Po += 1
                elif "Email" in cell: # detect if ticket type is on the next row
                    Found_Ticket_Type += 1
                elif Found_Ticket_Type == 1: 
                    ticket_type = cell # detect ticket type
                    Found_Ticket_Type += 1
                    
    # Format each product as a complete array with shared PO info
    formatted_products = []
    for idx, product in enumerate(product_details):
        # Clean OCR artifacts from all fields
        cleaned_product = [re.sub(r'[\[\]\|]', '', str(field)) for field in product]
        
        # Expected format after initial parsing: [line_num, product_num, description]
        # Target format: ['Grainger', po_number, line_num, product_num, description, ship_date, qty, price, ticket_type, address]
        formatted_product = ['Grainger', po_number]
        
        # Add product-specific details
        if len(cleaned_product) >= 3:
            formatted_product.append(cleaned_product[0])  # line number
            formatted_product.append(cleaned_product[1])  # product number
            formatted_product.append(cleaned_product[2])  # description
            
            # Add qty, date, price from collected lists
            if idx < len(date_list):
                formatted_product.append(date_list[idx])  # ship date
            else:
                formatted_product.append('')
                
            if idx < len(qty_list):
                formatted_product.append(qty_list[idx])  # qty
            else:
                formatted_product.append('')
                
            if idx < len(price_list):
                formatted_product.append(price_list[idx])  # price
            else:
                formatted_product.append('')  # Empty price if not found
        
        # Add shared details
        formatted_product.append(ticket_type)
        formatted_product.append(addr)
        
        formatted_products.append(formatted_product)
    
    # Write formatted CSV to csv_example directory, overwriting if exists
    out_dir = r"C:\\Users\\joseph.stadum\\lt_aimbot\\csv_example"
    os.makedirs(out_dir, exist_ok=True)
    out_name = os.path.splitext(os.path.basename(file_name))[0] + ".csv"
    out_path = os.path.join(out_dir, out_name)
    with open(out_path, "w", newline="", encoding="utf-8") as out_csv:
        w = csv.writer(out_csv)
        # Rows (no header)
        for product in formatted_products:
            w.writerow(product)
    
    return formatted_products
# code to check and move the date if necessary
def is_date(string):
    try:
        datetime.strptime(string, "%M/%D/%Y")
        return True
    except ValueError:
        return False
    
def move_to_wed(date_obj):
    date_obj = datetime.strptime(date_str, "%M/%D/%Y")

    if date_obj.weekday() != 2:
        days_ahead = (2 - date_obj.weekday() + 7) % 7
        if days_ahead == 0:
            date_ahead = 7
        date_obj += timedelta(days=day_ahead)

    return date_obj.strftime("%M/%D/%Y")

def is_format(value):
    s = str(value)
    result = len(s) == 6 and s.startswith("(0000") and s[-1].isdigit()
    return result

# take in file path as argument
arg1 = ""
if len(sys.argv) > 1:
    arg1 = sys.argv[1]
    print(f"First argument: {arg1}")
    products = process_file(arg1)
    for product in products:
        print(product)
else:
    print("No arguments provided")
# PATH = "C:\\Users\\joseph.stadum\\pdf_to_csv\\output\\Grainger - PO No 4647325819.csv"


