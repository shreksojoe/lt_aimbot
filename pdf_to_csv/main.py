import os
import csv
from pdf2image import convert_from_path
import pytesseract
import data

import csv_sort

# ====== Configuration Variables ======
def convert(filename):

    # INPUT_FOLDER = r"C:\\Users\\joseph.stadum\\Downloads\\Grainger" # stores pdfs
    # Write OCR CSVs to the shared csv_example directory
    OUTPUT_FOLDER = r"C:\\Users\\joseph.stadum\\lt_aimbot\\csv_example"  # stores converted csvs
    POPPLER_PATH = r"C:\\Users\\joseph.stadum\\poppler\\poppler-25.07.0\\Library\\bin"  #path to poppler 
    TESSERACT_PATH = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  #path to tesseract 

    # Set pytesseract executable path
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Process each PDF in the input folder
    # for filename in os.listdir(INPUT_FOLDER):
    # pdf_path = os.path.join(INPUT_FOLDER, filename)
    # print(f"Processing {filename}...")

    # Convert PDF pages to images
    images = convert_from_path(filename, poppler_path=POPPLER_PATH)

    # Prepare CSV file path
    # Use only the base filename for output
    csv_filename = os.path.splitext(os.path.basename(filename))[0] + ".csv"
    csv_path = os.path.join(OUTPUT_FOLDER, csv_filename)

    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        for page_number, image in enumerate(images, start=1):
            # Use pytesseract to extract text line by line
            text = pytesseract.image_to_string(image)
            lines = text.splitlines()

            for line in lines:
                if line.strip():  # skip empty lines
                    # Split line by whitespace into multiple cells
                    row = line.split()
                    writer.writerow(row)

    print(f"Saved CSV to {csv_path}")
    return csv_sort.process_file(csv_path)

