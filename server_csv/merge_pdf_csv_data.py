import os
import pandas as pd
import json

# Folders
text_folder = "text_data"   # PDF text files (.txt)
csv_folder = "csv_data"     # CSV output files (.csv)
output_file = "dataset.jsonl"  # Final JSONL file

# Ensure output file is empty
with open(output_file, "w") as out_f:
    pass

# Loop through all text files
for txt_file in os.listdir(text_folder):
    if txt_file.endswith(".txt"):
        # Corresponding CSV filename
        csv_file = txt_file.replace(".txt", ".csv")
        csv_path = os.path.join(csv_folder, csv_file)
        txt_path = os.path.join(text_folder, txt_file)

        # Skip if CSV does not exist
        if not os.path.exists(csv_path):
            print(f"Skipping {txt_file}, no corresponding CSV found.")
            continue

        # Read PDF text
        with open(txt_path, "r", encoding="utf-8") as f:
            pdf_text = f.read()

        # Read CSV text
        df = pd.read_csv(csv_path)
        csv_text = df.to_csv(index=False)

        # Create JSON object
        data = {"input": pdf_text, "output": csv_text}

        # Append to JSONL
        with open(output_file, "a", encoding="utf-8") as out_f:
            out_f.write(json.dumps(data) + "\n")

print(f"Done! JSONL dataset saved as {output_file}")
