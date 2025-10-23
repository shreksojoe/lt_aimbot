import os
import re
import csv
from typing import List, Tuple, Optional

# Deterministic parser for Grainger PO TXT -> CSV
# Output schema per examples in server_csv/csv_data/:
# COMPANY, PO, LINE, PART, DESCRIPTION, SHIP_DATE, QUANTITY, PRICE, BRAND, ADDRESS
# COMPANY is always "Grainger"; BRAND appears as constant "iStock" in examples.

COMPANY = "Grainger"
# BRAND will be determined per row based on ship-to address content

LINE_ITEM_RE = re.compile(r"^\s*(?P<line>\d{5})\s+(?P<part>\S+)\s+(?P<rest>.+?)\s*$")
# Match quantity with optional slash: "14 Each" or "14/Each"
QTY_RE = re.compile(r"(?P<qty>\d+)\s*/\s*Each|(?P<qty2>\d+)\s+Each")
DECIMAL_RE = re.compile(r"(\d+\.\d{1,2})")
# Pack-size tokens appear in descriptions like PK1000, PK250, etc.
PACK_RE = re.compile(r"\bPK\s*\d+\b", re.IGNORECASE)
SHIP_DATE_RE = re.compile(r"Promised\s+Ship\s+Date:\s*(?P<date>\d{1,2}/\d{1,2}/\d{4})")
TEN_DIGIT_RE = re.compile(r"\b(\d{10})\b")
CITY_STATE_ZIP_RE = re.compile(r"\b[A-Z]{2}\s+\d{5}(?:-\d{4})?\b")

# Explicit '<ST> <ZIP> <COUNTRY>' detector (country can be US/USA/UNITED STATES)
STATE_ZIP_COUNTRY_RE = re.compile(
    r"\b([A-Z]{2})\s+(\d{5}(?:-\d{4})?)\s+(US|USA|UNITED STATES)\b",
    re.IGNORECASE,
)

# Two-letter US state codes (exclude 'US'). Used to optionally insert a newline before state.
STATE_CODES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"
}

# Some texts have vendor and ship-to on one line, e.g. "ROLL PRODUCTS INC. WW GRAINGER FOUNTAIN INN"
# Strip the vendor prefix to leave the Ship-To party name.
VENDOR_PREFIXES = [
    "ROLL PRODUCTS INC.",
]


def clean_ocr_noise(text: str) -> str:
    text = re.sub(r"[\[\]\(\)]", "", text)
    fixed_lines: List[str] = []
    for ln in text.splitlines():
        s = ln
        s = re.sub(r"^\s*I(?=[A-Z])", "", s)
        s = re.sub(r"(\d)\|\s*Each", r"\1 Each", s)
        s = re.sub(r"(\d)\\\s*Each", r"\1 Each", s)
        s = s.replace("|", "")
        s = s.replace("\\", "")
        fixed_lines.append(s)
    return "\n".join(fixed_lines)


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
    # Line +1: name (strip vendor prefixes)
    if idx + 1 < len(lines):
        name_line = lines[idx + 1].strip()
        for vp in VENDOR_PREFIXES:
            if vp in name_line:
                name_line = name_line.split(vp, 1)[1].strip()
                break
        if name_line:
            parts.append(name_line)

    # Lookahead window and targets
    start = idx + 2
    end = min(len(lines), idx + 15)
    city_idx = None

    # Pass 1: locate FIRST city/state/zip line
    for j in range(start, end):
        raw = lines[j]
        if not raw:
            continue
        up = raw.strip().upper()
        if "SHIP-TO QUALIFIER" in up or up.startswith("CODE:"):
            continue
        if CITY_STATE_ZIP_RE.search(raw):
            city_idx = j
            break

    # Pass 2: starting from the city line, locate the FIRST country token (exact or embedded)
    country_idx = None
    country_embedded = False
    country_trim = None
    search_start = city_idx if city_idx is not None else start
    for j in range(search_start, end):
        raw = lines[j]
        if not raw:
            continue
        up = raw.strip().upper()
        if "SHIP-TO QUALIFIER" in up or up.startswith("CODE:"):
            break
        # If the same line contains '<ST> <ZIP> <COUNTRY>', trim at match start and stop
        m_szc = STATE_ZIP_COUNTRY_RE.search(raw)
        if m_szc:
            country_idx = j
            country_embedded = True
            country_trim = raw[:m_szc.start()].rstrip(', ')
            break
        # Exact country line
        if up in ("US", "USA", "UNITED STATES"):
            country_idx = j
            country_embedded = False
            country_trim = None
            break
        # Embedded country token (ensure it occurs AFTER city_idx or when city not yet found)
        for token in (" UNITED STATES", " USA", " US"):
            pos = up.find(token)
            if pos != -1:
                country_idx = j
                country_embedded = True
                country_trim = raw[:pos].rstrip(', ')
                break
        if country_idx is not None:
            break

    # Decide stop point: prefer city line; then include first country AFTER city if present
    stop_at = None
    include_country = False
    if city_idx is not None:
        stop_at = city_idx
    else:
        # no city found, fallback logic uses a few lines
        stop_at = None

    if country_idx is not None and (city_idx is None or country_idx >= city_idx):
        stop_at = country_idx
        include_country = True
    else:
        # Fallback: take up to 3 non-empty, non-qualifier lines
        taken = 0
        for j in range(start, end):
            ln = lines[j].strip()
            if not ln:
                continue
            up = ln.upper()
            if "SHIP-TO QUALIFIER" in up or up.startswith("CODE:"):
                break
            parts.append(ln)
            taken += 1
            if taken >= 3:
                break
        address = normalize_spaces(" ".join(p for p in parts if p))
        return address or None

    # Second pass: collect lines from start up to stop_at
    for j in range(start, (stop_at + 1) if stop_at is not None else end):
        ln = lines[j].strip()
        if not ln:
            continue
        up = ln.upper()
        if "SHIP-TO QUALIFIER" in up or up.startswith("CODE:"):
            break
        if stop_at is not None and j == country_idx and country_embedded:
            if country_trim:
                parts.append(country_trim)
            continue  # country will be appended below uniformly
        # If exact country line, skip its content (we add canonical 'US' below)
        if stop_at is not None and j == country_idx and not country_embedded:
            continue
        parts.append(ln)

    if include_country:
        parts.append("US")
    elif city_idx is not None:
        # If we stopped at city/state/zip and the very next few lines contain a country token, include it
        lookahead_limit = min(len(lines), city_idx + 4)
        for k in range(city_idx + 1, lookahead_limit):
            nxt = lines[k].strip()
            if not nxt:
                continue
            upn = nxt.upper()
            if "SHIP-TO QUALIFIER" in upn or upn.startswith("CODE:"):
                break
            if upn in ("US", "USA", "UNITED STATES"):
                parts.append("US")
                break

    # Normalize each line and split state/zip/country onto separate lines
    norm_parts = [normalize_spaces(p) for p in parts if p]
    
    # Merge first two lines (name + street) into one line
    if len(norm_parts) >= 2:
        merged_first = f"{norm_parts[0]} {norm_parts[1]}"
        norm_parts = [merged_first] + norm_parts[2:]
    
    # Split any line containing "<City>, <ST> <ZIP>" into separate lines
    final_parts = []
    for part in norm_parts:
        # Check if this line has state/zip pattern
        m = re.search(r"^(.+),\s+([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$", part)
        if m and m.group(2) in STATE_CODES:
            # Split into: city (without comma), state, zip
            city = m.group(1)
            state = m.group(2)
            zip_code = m.group(3)
            final_parts.append(city)
            final_parts.append(state)
            final_parts.append(zip_code)
        else:
            final_parts.append(part)
    
    address = "\n".join(final_parts)
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
    # Handle both qty groups (slash or space)
    qty = qty_m.group("qty") or qty_m.group("qty2")

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
    
    # Try to capture pack-size token BEFORE stripping trailing numbers
    pack_token = None
    # Check for trailing numbers after comma (e.g., ",1000") in raw desc_region
    trailing_num = re.search(r",\s*(\d{3,5})\s*$", desc_region)
    if trailing_num:
        pack_token = trailing_num.group(1)
    # Search for PK#### pattern in 'rest' around description
    if not pack_token:
        mpack = PACK_RE.search(rest)
        if not mpack and i + 1 < len(lines):
            mpack = PACK_RE.search(lines[i + 1])
        if mpack:
            pack_token = mpack.group(0).upper().replace(" ", "")  # Normalize e.g., PK 1000 -> PK1000
    
    # Remove trailing price numbers if mistakenly included (but preserve pack if already captured)
    # Heuristic: strip any trailing numbers/decimals that look like prices
    desc_region = re.sub(r"\s+(\d+\.\d{1,2})\s*$", "", desc_region)
    description = normalize_spaces(desc_region)
    
    # If pack token was found but not in description, add it
    if pack_token and pack_token not in description.replace(" ", "").replace(",", ""):
        # If description ends with a bare ',PK', replace it with ',PK####'
        if description.rstrip().upper().endswith(',PK'):
            description = re.sub(r",\s*PK\s*$", f",{pack_token}", description, flags=re.IGNORECASE)
        elif not description.endswith(pack_token):
            # Otherwise append with comma if not already there
            if not description.endswith(','):
                description = f"{description},"
            description = f"{description}{pack_token}"

    # Ship date: search in subsequent lines until next line item or a cap
    j = i + 1
    next_item_idx = find_next_line_item_idx(lines, i + 1)
    ship_date = None
    for k in range(i, min(next_item_idx, i + 30)):
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
            # Determine brand from address: if Ship-To contains GRAINGER, treat as iStock; otherwise Drop Ship
            brand = "iStock" if "GRAINGER" in address.upper() else "Drop Ship"

            row = [
                COMPANY,
                po,
                line_no,
                part,
                desc,
                ship_date,
                qty,
                price,
                brand,
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
    text = clean_ocr_noise(text)
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


def interactive_menu():
    """Interactive menu for selecting input and output paths."""
    print("\n=== Grainger PO TXT to CSV Converter ===")
    print("1. Convert a single .txt file")
    print("2. Convert all .txt files in a folder")
    print("3. Exit")
    
    choice = input("\nSelect an option (1-3): ").strip()
    
    if choice == "1":
        in_path = input("Enter path to .txt file: ").strip()
        if not os.path.isfile(in_path):
            print(f"Error: File not found: {in_path}")
            return
        out_folder = input("Enter output folder (press Enter for same folder as input): ").strip()
        if not out_folder:
            out_folder = os.path.dirname(in_path) or "."
        out_path = os.path.join(out_folder, os.path.splitext(os.path.basename(in_path))[0] + ".csv")
        rows = convert_file(in_path, out_path)
        print(f"\nConverted 1 file -> {rows} rows into {out_path}")
    
    elif choice == "2":
        in_folder = input("Enter input folder path: ").strip()
        if not os.path.isdir(in_folder):
            print(f"Error: Folder not found: {in_folder}")
            return
        out_folder = input("Enter output folder (press Enter for 'final_csv'): ").strip()
        if not out_folder:
            out_folder = "final_csv"
        files, rows = convert_folder(in_folder, out_folder)
        print(f"\nConverted {files} files -> {rows} rows into {out_folder}")
    
    elif choice == "3":
        print("Exiting...")
        return
    
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
        interactive_menu()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert Grainger PO TXT files to CSV rows.")
    parser.add_argument("input", nargs="?", help="Input .txt file or a folder containing .txt files")
    parser.add_argument("--out", help="Output folder for CSV files (for folder mode)")

    args = parser.parse_args()

    # If no arguments provided, launch interactive menu
    if not args.input:
        interactive_menu()
    elif os.path.isdir(args.input):
        out_folder = args.out if args.out else "final_csv"
        files, rows = convert_folder(args.input, out_folder)
        print(f"Converted {files} files -> {rows} rows into {out_folder}")
    else:
        in_path = args.input
        base_out_dir = args.out if args.out else os.path.dirname(in_path) or "."
        out_path = os.path.join(base_out_dir, os.path.splitext(os.path.basename(in_path))[0] + ".csv")
        rows = convert_file(in_path, out_path)
        print(f"Converted 1 file -> {rows} rows into {out_path}")
