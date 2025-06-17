import pandas as pd
import os
import sys

def convert(xlsx_file):
    # load file
    load_file = pd.read_excel(xlsx_file)
    
    base_name = os.path.splitext(xlsx_file)[0]

    csv_path = f"{base_name}.csv"
    
    load_file.to_csv(csv_path, index=False, encoding='utf-8-sig')

    return csv_path

