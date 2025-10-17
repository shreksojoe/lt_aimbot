import spacy
from spacy.tokens import DocBin
import json
import csv
from io import StringIO

nlp = spacy.blank("en")
db = DocBin()
db_dev = DocBin()

# Define field-to-label mapping based on your CSV output
FIELD_LABELS = [
    ("COMPANY", "COMPANY"),
    ("PO", "PO"),
    ("LINE", "LINE"),
    ("PART", "PART"),
    ("DESCRIPTION", "DESCRIPTION"),
    ("SHIP_DATE", "SHIP_DATE"),
    ("QUANTITY", "QUANTITY"),
    ("PRICE", "PRICE"),
    ("BRAND", "BRAND"),
    ("ADDRESS", "ADDRESS")
]

# Load dataset.jsonl
with open("dataset.jsonl", "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]

# Split 80/20
train_data = data[:80]
dev_data = data[80:]

# Process training data
for item in train_data:
    text = item["input"]
    csv_str = item["output"].strip()
    doc = nlp.make_doc(text)
    ents = []
    
    # Parse CSV output
    csv_reader = csv.reader(StringIO(csv_str), delimiter=',', quotechar='"')
    fields = next(csv_reader)  # Get first row
    
    # Map fields to text spans
    for i, (csv_field, label) in enumerate(FIELD_LABELS):
        if i < len(fields):
            value = fields[i].strip()
            if value:
                # Find exact match in text (case-sensitive)
                start = text.find(value)
                if start != -1:
                    end = start + len(value)
                    span = doc.char_span(start, end, label=label)
                    if span:
                        ents.append(span)
    
    # Add valid entities
    if ents:
        doc.ents = ents
        db.add(doc)

# Process dev data
for item in dev_data:
    text = item["input"]
    csv_str = item["output"].strip()
    doc = nlp.make_doc(text)
    ents = []
    
    csv_reader = csv.reader(StringIO(csv_str), delimiter=',', quotechar='"')
    fields = next(csv_reader)
    
    for i, (csv_field, label) in enumerate(FIELD_LABELS):
        if i < len(fields):
            value = fields[i].strip()
            if value:
                start = text.find(value)
                if start != -1:
                    end = start + len(value)
                    span = doc.char_span(start, end, label=label)
                    if span:
                        ents.append(span)
    
    if ents:
        doc.ents = ents
        db_dev.add(doc)

# Save
db.to_disk("train.spacy")
db_dev.to_disk("dev.spacy")
print(f"Created train.spacy ({len(db)} docs), dev.spacy ({len(db_dev)} docs)")
