import os
import sys

def extract_text(pdf_path: str) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join((page.extract_text() or "") for page in pdf.pages)
        if text.strip():
            return text
    except Exception:
        pass

    try:
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(pdf_path)
        parts = []
        for i in range(len(doc)):
            page = doc[i]
            textpage = page.get_textpage()
            parts.append(textpage.get_text_range())
        text = "\n".join(parts)
        if text.strip():
            return text
    except Exception:
        pass

    try:
        import pypdfium2 as pdfium
        import pytesseract
        from PIL import Image  # Pillow is present via pdfplumber dependency
        doc = pdfium.PdfDocument(pdf_path)
        parts = []
        for i in range(len(doc)):
            page = doc[i]
            bmp = page.render(scale=2).to_pil()
            parts.append(pytesseract.image_to_string(bmp))
        return "\n".join(parts)
    except Exception:
        return ""

if len(sys.argv) != 3:
    print("Usage: python llama_trainer.py input.pdf output.txt")
    sys.exit(1)

pdf_path = sys.argv[1]
txt_path = sys.argv[2]

text = extract_text(pdf_path)

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(text)
