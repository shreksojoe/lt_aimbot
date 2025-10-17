import os
import re
import csv
from typing import List, Tuple, Optional

# Deterministic parser for Grainger PO TXT -> CSV
# Output schema per examples in server_csv/csv_data/:
# COMPANY, PO, LINE, PART, DESCRIPTION, SHIP_DATE, QUANTITY, PRICE, BRAND, ADDRESS
# COMPANY is always "Grainger"; BRAND appears as constant "iStock" in examples.

COMPANY = "Grainger"
BRAND = "iStock"

LINE_ITEM_RE = re.compile(r"^\s*(?P<line>\d{5})\s+(?P<part>\S+)\s+(?P<rest>.+?)\s*$")
QTY_RE = re.compile(r"(?P<qty>\d+)\s*Each")
DECIMAL_RE = re.compile(r"(\d+\.\d{2})")
SHIP_DATE_RE = re.compile(r"Promised\s+Ship\s+Date:\s*(?P<date>\d{1,2}/\d{1,2}/\d{4})")
TEN_DIGIT_RE = re.compile(r"\b(\d{10})\b")

# Some texts have vendor and ship-to on one line, e.g. "ROLL PRODUCTS INC. WW GRAINGER FOUNTAIN INN"
# Strip the vendor prefix to leave the Ship-To party name.
VENDOR_PREFIXES = [
    "ROLL PRODUCTS INC.",
]


def normalize_spaces(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    # Fix spaced commas like "FOUNTAIN INN , SC" -> "FOUNTAIN INN, SC"
    s = re.sub(r"\s+,\s*", ", ", s)
    return s


def extract_po_number(text: str) -> Optional[str]:
    # Use the first 10-digit token as PO
    m = TEN_DIGIT_RE.search(text)
    return m.group(1) if m else None


def extract_ship_to_address(lines: List[str]) -> Optional[str]:
    # Find the "Vendor: Ship To:" line, then capture the next 3-4 lines
    # Expected layout after that marker:
    # line+1: "ROLL PRODUCTS INC. <SHIP_TO_NAME>"
    # line+2: <street>
    # line+3: <city> , <state> <zip>
    # line+4: US
    idx = None
    for i, ln in enumerate(lines):
        if "Vendor: Ship To:" in ln:
            idx = i
            break
    if idx is None:
        return None
    parts: List[str] = []
    if idx + 1 < len(lines):
        name_line = lines[idx + 1].strip()
        # Remove vendor prefixes
        for vp in VENDOR_PREFIXES:
            if vp in name_line:
                name_line = name_line.split(vp, 1)[1].strip()
                break
        if name_line:
            parts.append(name_line)
    if idx + 2 < len(lines):
        parts.append(lines[idx + 2].strip())
    if idx + 3 < len(lines):
        parts.append(lines[idx + 3].strip())
    if idx + 4 < len(lines):
        parts.append(lines[idx + 4].strip())
    address = normalize_spaces(" ".join(p for p in parts if p))
    return address or None


def find_next_line_item_idx(lines: List[str], start: int) -> int:
    for j in range(start, len(lines)):
        if LINE_ITEM_RE.match(lines[j]):
            return j
    return len(lines)


def parse_line_item(lines: List[str], i: int) -> Tuple[Optional[Tuple[str, str, str, str, str, str]], int]:
    """
    Returns: ((line, part, description, ship_date, quantity, price), next_index_after_item)
    or (None, next_index) if not parseable.
    """
    m = LINE_ITEM_RE.match(lines[i])
    if not m:
        return None, i + 1
    line_no = m.group("line")
    part = m.group("part")
    rest = m.group("rest")

    # Quantity: first qty occurrence (\d+Each)
    qty_m = QTY_RE.search(rest)
    if not qty_m:
        # Sometimes qty might be on next line (rare) — include next line for search
        if i + 1 < len(lines):
            ext = rest + " " + lines[i + 1]
            qty_m = QTY_RE.search(ext)
            if qty_m:
                rest = ext
    if not qty_m:
        return None, i + 1
    qty = qty_m.group("qty")

    # Find decimals in the same region; expect unit price and amount
    decimals = DECIMAL_RE.findall(rest)
    unit_price = None
    if len(decimals) >= 2:
        unit_price = decimals[-2]
    elif len(decimals) == 1:
        unit_price = decimals[0]

    # Description: substring between the end of part token and the qty occurrence
    # Locate the first occurrence position of qty match in the current rest string
    qty_span = qty_m.span()
    # But qty_m was searched in 'rest' or 'ext'. If in 'ext', ensure description from rest start to qty start
    desc_region = rest[:qty_span[0]]
    # Remove trailing price numbers if mistakenly included
    # Heuristic: strip any trailing numbers/decimals
    desc_region = re.sub(r"\s*(\d+\.?\d*)\s*$", "", desc_region)
    description = normalize_spaces(desc_region)

    # Ship date: search in subsequent lines until next line item or a cap
    j = i + 1
    next_item_idx = find_next_line_item_idx(lines, i + 1)
    ship_date = None
    for k in range(i, min(next_item_idx, i + 10)):
        mdate = SHIP_DATE_RE.search(lines[k])
        if mdate:
            ship_date = mdate.group("date")
            break
    if ship_date is None:
        # Sometimes on the same line concatenated (e.g., "EachPromised Ship Date:")
        mdate = SHIP_DATE_RE.search(rest)
        if mdate:
            ship_date = mdate.group("date")

    if not unit_price:
        # Try next line for price decimals if not found
        if i + 1 < len(lines):
            decimals2 = DECIMAL_RE.findall(lines[i + 1])
            if decimals2:
                unit_price = decimals2[0]

    if not (line_no and part and description and qty and unit_price):
        return None, max(i + 1, next_item_idx)

    return (line_no, part, description, ship_date or "", qty, unit_price), max(i + 1, next_item_idx)


def parse_txt_to_rows(text: str) -> List[List[str]]:
    lines = [ln.rstrip("\n") for ln in text.splitlines()]

    po = extract_po_number(text) or ""
    address = extract_ship_to_address(lines) or ""

    rows: List[List[str]] = []

    i = 0
    while i < len(lines):
        # Scan for line items and parse
        itm, nxt = parse_line_item(lines, i)
        if itm:
            line_no, part, desc, ship_date, qty, price = itm
            row = [
                COMPANY,
                po,
                line_no,
                part,
                desc,
                ship_date,
                qty,
                price,
                BRAND,
                address,
            ]
            rows.append(row)
            i = nxt
        else:
            i += 1
    return rows


def convert_file(in_path: str, out_path: str) -> int:
    with open(in_path, "r", encoding="utf-8") as f:
        text = f.read()
    rows = parse_txt_to_rows(text)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for r in rows:
            writer.writerow(r)
    return len(rows)


def convert_folder(in_dir: str, out_dir: str) -> Tuple[int, int]:
    total = 0
    files = 0
    for name in os.listdir(in_dir):
        if not name.lower().endswith(".txt"):
            continue
        files += 1
        src = os.path.join(in_dir, name)
        dst = os.path.join(out_dir, os.path.splitext(name)[0] + ".csv")
        total += convert_file(src, dst)
    return files, total


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert Grainger PO TXT files to CSV rows.")
    parser.add_argument("input", nargs="?", default="text_data", help="Input .txt file or a folder containing .txt files")
    parser.add_argument("--out", default="final_csv", help="Output folder for CSV files (for folder mode)")

    args = parser.parse_args()

    if os.path.isdir(args.input):
        files, rows = convert_folder(args.input, args.out)
        print(f"Converted {files} files -> {rows} rows into {args.out}")
    else:
        in_path = args.input
        base_out_dir = args.out if args.out else os.path.dirname(in_path) or "."
        out_path = os.path.join(base_out_dir, os.path.splitext(os.path.basename(in_path))[0] + ".csv")
        rows = convert_file(in_path, out_path)
        print(f"Converted 1 file -> {rows} rows into {out_path}")
