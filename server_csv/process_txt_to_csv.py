import spacy
import pandas as pd
import os
from spacy.matcher import Matcher, PhraseMatcher

# Load fine-tuned model
nlp = spacy.load("./my_model/model-best")

# Folders
text_dir = "text_data"
csv_dir = "final_csv"  # Updated folder
os.makedirs(csv_dir, exist_ok=True)

# CSV columns (for internal use only; no headers in output)
columns = ["COMPANY", "PO", "LINE", "PART", "DESCRIPTION", "SHIP_DATE", "QUANTITY", "PRICE", "BRAND", "ADDRESS"]

# Process each .txt file
for txt_file in os.listdir(text_dir):
    if txt_file.endswith(".txt"):
        with open(os.path.join(text_dir, txt_file), "r", encoding="utf-8") as f:
            text = f.read().strip()
        
        # Normalize text for better matching (remove extra newlines, normalize spaces)
        text = " ".join(text.split())
        
        doc = nlp(text)
        row = {col: "" for col in columns}  # Initialize all fields
        
        # Extract from NER
        for ent in doc.ents:
            if ent.label_ in row:
                row[ent.label_] = ent.text
        
        # Debug: Print NER extractions
        print(f"NER extractions for {txt_file}: {row}")
        
        # Fallback rules with Matcher
        matcher = Matcher(nlp.vocab)
        # Address: Very flexible - after "Ship To:" or "Vendor:" or "ROLL PRODUCTS INC.", capture block with street/city/state/ZIP/US (handles normalized text)
        matcher.add("ADDRESS", [
            [{"TEXT": "Ship"}, {"TEXT": "To:"}, {"OP": "*"}, {"LIKE_NUM": True}, {"OP": "*"}, {"TEXT": {"REGEX": r"(FACILITIES|SUPPLY|Dr|Blvd|Ave|Rd|St|Hubbard|Southchase|Dearborn|FOUNTAIN|INN)"}}, {"OP": "*"}, {"TEXT": {"REGEX": r"[A-Z]{2}"}}, {"LIKE_NUM": True}, {"TEXT": "US"}],
            [{"TEXT": "Vendor:"}, {"OP": "*"}, {"TEXT": "ROLL"}, {"TEXT": "PRODUCTS"}, {"TEXT": "INC."}, {"OP": "*"}, {"LIKE_NUM": True}, {"OP": "*"}, {"TEXT": {"REGEX": r"(Dr|Blvd|Ave|Rd|St|Hubbard|Southchase|Dearborn|FOUNTAIN|INN)"}}, {"OP": "*"}, {"TEXT": {"REGEX": r"[A-Z]{2}"}}, {"LIKE_NUM": True}, {"TEXT": "US"}],
            [{"TEXT": "ROLL"}, {"TEXT": "PRODUCTS"}, {"TEXT": "INC."}, {"OP": "*"}, {"LIKE_NUM": True}, {"OP": "*"}, {"TEXT": {"REGEX": r"(Dr|Blvd|Ave|Rd|St|Hubbard|Southchase|Dearborn|FOUNTAIN|INN)"}}, {"OP": "*"}, {"TEXT": {"REGEX": r"[A-Z]{2}"}}, {"LIKE_NUM": True}, {"TEXT": "US"}]
        ])
        # PhraseMatcher for known address snippets (to handle variations)
        phrase_matcher = PhraseMatcher(nlp.vocab)
        address_phrases = nlp.pipe(["NON-CLINICAL SUPPLY", "19401 Hubbard Dr", "101 SOUTHCHASE BLVD", "Dearborn , MI 48126", "FOUNTAIN INN , SC 29644", "FACILITIES - RECEIVI", "0014289069"])  # Common from samples
        phrase_matcher.add("ADDRESS_PHRASE", list(address_phrases))
        
        # PO: 10-digit number
        matcher.add("PO", [[{"TEXT": {"REGEX": r"\d{10}"}}]])
        # SHIP_DATE: MM/DD/YYYY
        matcher.add("SHIP_DATE", [[{"TEXT": {"REGEX": r"\d{1,2}/\d{1,2}/\d{4}"}}]])
        # QUANTITY: Number before/after "Each" or "Qty"
        matcher.add("QUANTITY", [
            [{"TEXT": "Qty"}, {"OP": "?"}, {"LIKE_NUM": True}, {"TEXT": "Each"}],
            [{"LIKE_NUM": True}, {"TEXT": "Each"}]
        ])
        # PRICE: Decimal after quantity or "Amount"
        matcher.add("PRICE", [
            [{"TEXT": "Each"}, {"LIKE_NUM": True}, {"TEXT": {"REGEX": r"\d+\.\d{2}"}}],
            [{"TEXT": "Amount"}, {"TEXT": {"REGEX": r"\d+\.\d{2}"}}]
        ])
        # BRAND: After "Brand" or "Organization"
        matcher.add("BRAND", [[{"TEXT": "Brand"}, {"OP": "+"}, {"IS_ALPHA": True}], [{"TEXT": "Organization"}, {"OP": "+"}, {"IS_ALPHA": True}]])

        matches = matcher(doc)
        # Add phrase matcher matches (fixed: no as_doc())
        matches += phrase_matcher(doc)
        
        # Debug: Print matches
        print(f"Matcher matches for {txt_file}: {[(nlp.vocab.strings[match_id], doc[start:end].text) for match_id, start, end in matches]}")
        
        for match_id, start, end in matches:
            label = nlp.vocab.strings[match_id]
            if label in row and not row[label]:  # Only fill if NER missed it
                extracted = doc[start:end].text.strip()
                if label == "ADDRESS" or label == "ADDRESS_PHRASE":
                    extracted = extracted.replace("Ship To:", "").replace("Vendor:", "").replace("ROLL PRODUCTS INC.", "").strip()  # Trim extras
                    row["ADDRESS"] = extracted  # Set or append
                elif label == "QUANTITY":
                    extracted = extracted.split("Each")[0].strip() if "Each" in extracted else extracted.split()[-1]
                elif label == "PRICE":
                    extracted = extracted.split()[-1]  # Get decimal
                elif label == "BRAND":
                    extracted = extracted.split("Brand")[-1].strip() if "Brand" in extracted else extracted
                row[label] = extracted
        
        # Debug: Print final row before saving
        print(f"Final row for {txt_file}: {row}")
        
        if any(row.values()):  # Save if any field populated
            df = pd.DataFrame([row], columns=columns)
            csv_path = os.path.join(csv_dir, txt_file.replace(".txt", ".csv"))
            df.to_csv(csv_path, index=False, header=False)  # No headers
            print(f"Saved {csv_path}")
