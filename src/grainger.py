import window
import motion
import data

import importlib.util
import csv
import sys
import os


# Pipeline -- convert to csv
# run pdf through pdf_to_csv (output is a csv) -- works
# write json files
# 
# 
# 
# 
# 
# 
# 
# 


def execute_grainger(grainger_pdf):
    pdf_path = data.find_rel_path(r"pdf_to_csv\\main.py")
    
    # Add pdf_to_csv directory to sys.path so imports work
    pdf_dir = os.path.dirname(pdf_path)
    if pdf_dir not in sys.path:
        sys.path.insert(0, pdf_dir)

    spec = importlib.util.spec_from_file_location("pdf_module", pdf_path)
    pdf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pdf_module)
    
    print("converting to csv")
    csv_contents = pdf_module.convert(grainger_pdf)
    print("printing the csv")
    # print(csv_contents)
    for layer in csv_contents:
        print(layer)
    print("done converting pdf")
