import pdfplumber
import os

pdf_folder = "pdf_data\\"
text_folder = "text_data\\"

os.makedirs(text_folder, exist_ok=True)

for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        path = os.path.join(pdf_folder, pdf_file)
        with pdfplumber.open(path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        out_file = os.path.join(text_folder, pdf_file.replace(".pdf", ".txt"))
        with open(out_file, "w") as f:
            f.write(text)
