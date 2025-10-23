import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import sys
import os

def pdf_to_txt(pdf_path, txt_path):
    try:
        # Initialize an empty string to store all text
        full_text = ""
        
        # First, try extracting text directly with pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n\n"
        
        # If no text was extracted, try OCR with pytesseract
        if not full_text.strip():
            print("No text found with direct extraction, attempting OCR...")
            # Convert PDF pages to images
            images = convert_from_path(pdf_path)
            for image in images:
                # Perform OCR on the image
                text = pytesseract.image_to_string(image)
                if text:
                    full_text += text + "\n\n"
        
        # If still no text, report the issue
        if not full_text.strip():
            print("Error: No text could be extracted from the PDF.")
            return
        
        # Write the extracted text to a .txt file
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(full_text)
        
        print(f"Successfully converted {pdf_path} to {txt_path}")
    
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_txt_with_ocr.py <input_pdf> <output_txt>")
        sys.exit(1)
    
    # Get input and output file paths from command line arguments
    input_pdf = sys.argv[1]
    output_txt = sys.argv[2]
    
    # Call the conversion function
    pdf_to_txt(input_pdf, output_txt)
