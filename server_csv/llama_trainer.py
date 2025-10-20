import pdfplumber
import os
import sys

if len(sys.argv) != 3:
    print("Usage: python llama_trainer.py input.pdf output.txt")
    sys.exit(1)

pdf_path = sys.argv[1]
txt_path = sys.argv[2]

with pdfplumber.open(pdf_path) as pdf:
    text = "\n".join(page.extract_text() or "" for page in pdf.pages)

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(text)
