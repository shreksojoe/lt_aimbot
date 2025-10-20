import os
import sys
import traceback
import subprocess
import csv

SERVER_CSV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'server_csv'))
LLAMA_TRAINER = os.path.join(SERVER_CSV_DIR, 'llama_trainer.py')
TXT_TO_CSV = os.path.join(SERVER_CSV_DIR, 'txt_to_csv.py')
TEXT_DATA_DIR = os.path.join(SERVER_CSV_DIR, 'text_data')
FINAL_CSV_DIR = os.path.join(SERVER_CSV_DIR, 'final_csv')

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
    processed_count = 0
    error_count = 0

    # Ensure output dirs exist
    os.makedirs(TEXT_DATA_DIR, exist_ok=True)
    os.makedirs(FINAL_CSV_DIR, exist_ok=True)

    for pdf_path in file_paths:
        if not pdf_path.lower().endswith(".pdf"):
            print(f"- Skipping non-PDF: {pdf_path}")
            continue

        base = os.path.splitext(os.path.basename(pdf_path))[0]
        txt_path = os.path.join(TEXT_DATA_DIR, base + ".txt")
        csv_path = os.path.join(FINAL_CSV_DIR, base + ".csv")

        print(f"\n{'='*60}")
        print(f"Processing: {os.path.basename(pdf_path)}")
        print(f"{'-'*60}")

        try:
            # PDF -> TXT
            print(f"Running: llama_trainer.py -> {txt_path}")
            res1 = subprocess.run([sys.executable, LLAMA_TRAINER, pdf_path, txt_path], capture_output=True, text=True)
            if res1.returncode != 0:
                print(res1.stdout)
                print(res1.stderr)
                raise RuntimeError("llama_trainer failed")

            if not os.path.exists(txt_path):
                raise FileNotFoundError(f"TXT not created: {txt_path}")

            # TXT -> CSV
            print(f"Running: txt_to_csv.py -> {csv_path}")
            res2 = subprocess.run([sys.executable, TXT_TO_CSV, txt_path], capture_output=True, text=True, cwd=SERVER_CSV_DIR)
            if res2.returncode != 0:
                print(res2.stdout)
                print(res2.stderr)
                raise RuntimeError("txt_to_csv failed")

            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"CSV not created: {csv_path}")

            # Previews
            print("\n--- TXT Preview (first 40 lines) ---")
            try:
                with open(txt_path, "r", encoding="utf-8") as tf:
                    for i, line in enumerate(tf):
                        if i >= 40:
                            break
                        print(line.rstrip("\n"))
            except UnicodeDecodeError:
                with open(txt_path, "r", encoding="latin-1", errors="replace") as tf:
                    for i, line in enumerate(tf):
                        if i >= 40:
                            break
                        print(line.rstrip("\n"))

            print("\n--- CSV Preview (first 10 rows) ---")
            with open(csv_path, newline='', encoding='utf-8') as cf:
                reader = csv.reader(cf)
                for i, row in enumerate(reader):
                    if i >= 10:
                        break
                    print(row)

            print(f"\n✓ Done: {os.path.basename(pdf_path)}")
            print(f"TXT: {txt_path}")
            print(f"CSV: {csv_path}")
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
