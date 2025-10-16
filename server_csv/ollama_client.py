import os
import json
import pdfplumber
import pandas as pd
import requests

# CONFIGURATION

SERVER_URL = "http://192.168.1.128:11434"
CUSTOM_MODEL = "pdf-extractor"
PDF_FOLDER = r"C:\Users\joseph.stadum\lt_aimbot\server_csv\new_pdfs" 
OUTPUT_FOLDER = r"C:\Users\joseph.stadum\lt_aimbot\server_csv\output_csvs"

# FUNCTIONS

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

        return text.strip()

def process_new_pdfs():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for pdf_file in os.listdir(PDF_FOLDER):
        if not pdf_file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(PDF_FOLDER, pdf_file)
        pdf_text = extract_text_from_pdf(pdf_path)

        prompt = f"Extract structured CSV data from this PDF text:\n\n{pdf_text}\n\nCSV:"

        response = requests.post(
            f"{SERVER_URL}/api/generate",
            json={"model": CUSTOM_MODEL, "prompt": prompt},
            stream=False
        )

        if response.status_code == 200:
            # Split the response into lines (each line is a JSON object)
            lines = response.text.strip().splitlines()

            # Extract the 'response' field from each JSON line
            output = ""
            for line in lines:
                try:
                    data = json.loads(line)
                    output += data.get("response", "")
                except json.JSONDecodeError:
                    continue  # skip malformed lines

            # Save the final CSV
            output_path = os.path.join(OUTPUT_FOLDER, pdf_file.replace(".pdf", ".csv"))
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"✅ Processed {pdf_file} → {output_path}")

        else:
            print(f"❌ Failed to process {pdf_file}: {response.text}")

if __name__ == "__main__":
    process_new_pdfs()


