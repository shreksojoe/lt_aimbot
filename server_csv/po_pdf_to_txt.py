import os
import sys
from typing import Tuple

try:
    import pdfplumber  # type: ignore
except ModuleNotFoundError:
    print("Missing dependency: pdfplumber. Install with: pip install pdfplumber")
    sys.exit(2)


def convert_pdf_to_txt(pdf_path: str, txt_path: str) -> int:
    """
    Convert a single PDF to TXT using pdfplumber.
    Returns number of pages processed.
    """
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        text = "\n".join((page.extract_text() or "") for page in pages)
    os.makedirs(os.path.dirname(txt_path) or ".", exist_ok=True)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    return len(pages)


def convert_folder(in_dir: str, out_dir: str) -> Tuple[int, int]:
    """
    Convert all .pdf files in a folder (non-recursive) to TXT in out_dir.
    Returns (files_converted, total_pages).
    """
    files = 0
    pages_total = 0
    os.makedirs(out_dir, exist_ok=True)
    for name in os.listdir(in_dir):
        if not name.lower().endswith(".pdf"):
            continue
        files += 1
        pdf_path = os.path.join(in_dir, name)
        txt_name = os.path.splitext(name)[0] + ".txt"
        txt_path = os.path.join(out_dir, txt_name)
        pages_total += convert_pdf_to_txt(pdf_path, txt_path)
    return files, pages_total


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Convert Grainger PO PDFs to TXT using pdfplumber.")
    parser.add_argument("input", help="Input .pdf file or a folder containing .pdf files")
    parser.add_argument("--out", dest="out", default=None, help="Output TXT file (if input is file) or output folder (if input is folder). Default: alongside input or './text_data' for folders")

    args = parser.parse_args()

    in_path = args.input
    if os.path.isdir(in_path):
        out_dir = args.out or os.path.join(os.getcwd(), "text_data")
        files, pages = convert_folder(in_path, out_dir)
        print(f"Converted {files} PDF(s), total {pages} page(s) -> {out_dir}")
    else:
        if not in_path.lower().endswith(".pdf"):
            print("Input must be a .pdf file or a folder containing .pdf files")
            sys.exit(1)
        out_path = args.out
        if not out_path:
            base_dir = os.path.dirname(in_path) or "."
            out_path = os.path.join(base_dir, os.path.splitext(os.path.basename(in_path))[0] + ".txt")
        pages = convert_pdf_to_txt(in_path, out_path)
        print(f"Converted 1 PDF, {pages} page(s) -> {out_path}")


if __name__ == "__main__":
    main()
