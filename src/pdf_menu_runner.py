import os
import sys
import traceback

# Allow importing pdf_to_csv/main.py as a module
PDF_TO_CSV_DIR = os.path.join(os.path.dirname(__file__), '..', 'pdf_to_csv')
PDF_TO_CSV_DIR = os.path.abspath(PDF_TO_CSV_DIR)
if PDF_TO_CSV_DIR not in sys.path:
    sys.path.insert(0, PDF_TO_CSV_DIR)

# Import the convert function which:
# - OCRs the PDF -> raw CSV
# - Runs csv_sort.process_file() on that CSV
# - Returns the formatted product array
import importlib.util

def import_pdf_module():
    main_path = os.path.join(PDF_TO_CSV_DIR, 'main.py')
    spec = importlib.util.spec_from_file_location("pdf_module", main_path)
    pdf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pdf_module)
    return pdf_module

def choose_pdfs_with_dialog():
    # Use a native file open dialog
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        file_paths = filedialog.askopenfilenames(
            title="Select Grainger PDF files",
            filetypes=[("PDF files", "*.pdf")],
        )
        root.destroy()
        return list(file_paths)
    except Exception:
        return []

def choose_pdfs_fallback():
    print("Could not open a file dialog. Enter full paths to PDFs, one per line.")
    print("When finished, enter a blank line.")
    paths = []
    while True:
        p = input("> ").strip().strip('"')
        if not p:
            break
        if os.path.isfile(p) and p.lower().endswith(".pdf"):
            paths.append(p)
        else:
            print("  Skipped (not a valid .pdf file).")
    return paths

def process_pdfs(file_paths):
    pdf_module = import_pdf_module()
    processed_count = 0
    error_count = 0

    for pdf_path in file_paths:
        if not pdf_path.lower().endswith(".pdf"):
            print(f"- Skipping non-PDF: {pdf_path}")
            continue

        print(f"\n{'='*60}")
        print(f"Processing: {os.path.basename(pdf_path)}")
        print(f"{'-'*60}")

        try:
            product_array = pdf_module.convert(pdf_path)  # calls csv_sort under the hood
            print(f"Products found: {len(product_array)}")
            if product_array:
                # Print a sample row to confirm structure
                sample = product_array[0]
                print("Sample product row (10 fields expected):")
                print(sample)
            print(f"✓ Done: {os.path.basename(pdf_path)}")
            processed_count += 1
        except Exception as e:
            print(f"✗ Error: {e}")
            traceback.print_exc()
            print("Continuing to next file...\n")
            error_count += 1

    print(f"\n{'='*60}")
    print("PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Successfully processed: {processed_count} file(s)")
    print(f"Errors encountered:    {error_count} file(s)")
    print(f"Total selected:        {len(file_paths)}")
    print(f"{'='*60}\n")

def main():
    print("Select one or more PDF files to process...")
    files = choose_pdfs_with_dialog()
    if not files:
        print("File dialog failed or canceled.")
        files = choose_pdfs_fallback()

    if not files:
        print("No files selected. Exiting.")
        return

    process_pdfs(files)

if __name__ == "__main__":
    main()
