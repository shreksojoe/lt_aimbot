import os
import csv
import sys
import difflib
import re
import string
from typing import Tuple

# Default folders
DEFAULT_A = os.path.abspath(os.path.join(os.path.dirname(__file__), 'final_csv'))
DEFAULT_B = os.path.abspath(os.path.join(os.path.dirname(__file__), 'csv_data'))
DEFAULT_REPORT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'compare_report.csv'))

# Thresholds for flagging outliers
# A file is flagged if ANY of these conditions are met
ABS_SIZE_DIFF_THRESHOLD = 200        # bytes
REL_SIZE_DIFF_THRESHOLD = 0.20       # 20%
ROW_COUNT_DIFF_THRESHOLD = 3         # rows
SIMILARITY_MIN_THRESHOLD = 0.85      # difflib ratio below this is suspicious
NORMALIZED_SIM_MIN_THRESHOLD = 0.95  # stricter after stripping punctuation/whitespace

ENCODINGS = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]


def read_text_with_fallback(path: str) -> str:
    last_err = None
    for enc in ENCODINGS:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError as e:
            last_err = e
            continue
    # final fallback
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def read_csv_rows(path: str) -> Tuple[int, int]:
    """Return (row_count, total_chars) as a light-weight content proxy."""
    last_err = None
    for enc in ENCODINGS:
        try:
            with open(path, 'r', newline='', encoding=enc) as f:
                reader = csv.reader(f)
                rows = list(reader)
                row_count = len(rows)
                # Sum of joined row string lengths as a proxy for content size
                total_chars = sum(len(','.join(r)) for r in rows)
                return row_count, total_chars
        except UnicodeDecodeError as e:
            last_err = e
            continue
        except Exception:
            break
    # Fallback tolerant read
    with open(path, 'r', newline='', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        rows = list(reader)
        row_count = len(rows)
        total_chars = sum(len(','.join(r)) for r in rows)
        return row_count, total_chars


def similarity_ratio(text_a: str, text_b: str) -> float:
    # For performance on larger files, cap to first 200k chars each
    cap = 200_000
    a = text_a[:cap]
    b = text_b[:cap]
    return difflib.SequenceMatcher(None, a, b).ratio()


_punct_table = str.maketrans('', '', string.punctuation)

def normalize_text(s: str) -> str:
    """Lowercase, remove punctuation (quotes/commas/etc), and collapse whitespace.
    Keeps only alphanumerics and spaces to compare semantic content more directly.
    """
    # Remove punctuation
    s = s.translate(_punct_table)
    # Replace any non-alphanumeric with space
    s = re.sub(r"[^0-9a-zA-Z]+", " ", s)
    # Lowercase and collapse spaces
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

def normalized_similarity_ratio(text_a: str, text_b: str) -> float:
    cap = 200_000
    na = normalize_text(text_a)[:cap]
    nb = normalize_text(text_b)[:cap]
    if not na and not nb:
        return 1.0
    return difflib.SequenceMatcher(None, na, nb).ratio()


def compare_folders(folder_a: str, folder_b: str, report_path: str) -> None:
    files_a = {f for f in os.listdir(folder_a) if f.lower().endswith('.csv')}
    files_b = {f for f in os.listdir(folder_b) if f.lower().endswith('.csv')}

    common = sorted(files_a & files_b)
    only_a = sorted(files_a - files_b)
    only_b = sorted(files_b - files_a)

    rows = []

    # Header
    rows.append([
        'filename',
        'size_a', 'size_b', 'abs_size_diff', 'rel_size_diff',
        'rows_a', 'rows_b', 'abs_row_diff',
        'chars_a', 'chars_b', 'abs_chars_diff', 'rel_chars_diff',
        'similarity_ratio', 'normalized_similarity_ratio',
        'flag_abs_size', 'flag_rel_size', 'flag_row_diff', 'flag_similarity', 'flag_norm_similarity', 'is_outlier'
    ])

    print(f"Comparing A={folder_a}\n          B={folder_b}")

    for name in common:
        path_a = os.path.join(folder_a, name)
        path_b = os.path.join(folder_b, name)

        size_a = os.path.getsize(path_a)
        size_b = os.path.getsize(path_b)
        abs_size_diff = abs(size_a - size_b)
        rel_size_diff = (abs_size_diff / max(1, size_b)) if size_b else 0.0

        rows_a, chars_a = read_csv_rows(path_a)
        rows_b, chars_b = read_csv_rows(path_b)
        abs_row_diff = abs(rows_a - rows_b)
        abs_chars_diff = abs(chars_a - chars_b)
        rel_chars_diff = (abs_chars_diff / max(1, chars_b)) if chars_b else 0.0

        # lightweight similarity (expensive, so do only if initial signals show notable difference)
        sim_ratio = 1.0
        norm_sim_ratio = 1.0
        if rel_size_diff > 0.05 or abs_row_diff > 0 or rel_chars_diff > 0.05:
            try:
                text_a = read_text_with_fallback(path_a)
                text_b = read_text_with_fallback(path_b)
                sim_ratio = similarity_ratio(text_a, text_b)
                norm_sim_ratio = normalized_similarity_ratio(text_a, text_b)
            except Exception:
                sim_ratio = 0.0
                norm_sim_ratio = 0.0

        flag_abs_size = abs_size_diff > ABS_SIZE_DIFF_THRESHOLD
        flag_rel_size = rel_size_diff > REL_SIZE_DIFF_THRESHOLD
        flag_row_diff = abs_row_diff > ROW_COUNT_DIFF_THRESHOLD
        flag_similarity = sim_ratio < SIMILARITY_MIN_THRESHOLD
        flag_norm_similarity = norm_sim_ratio < NORMALIZED_SIM_MIN_THRESHOLD

        is_outlier = any([flag_abs_size, flag_rel_size, flag_row_diff, flag_similarity, flag_norm_similarity])

        rows.append([
            name,
            size_a, size_b, abs_size_diff, f"{rel_size_diff:.3f}",
            rows_a, rows_b, abs_row_diff,
            chars_a, chars_b, abs_chars_diff, f"{rel_chars_diff:.3f}",
            f"{sim_ratio:.3f}", f"{norm_sim_ratio:.3f}",
            int(flag_abs_size), int(flag_rel_size), int(flag_row_diff), int(flag_similarity), int(flag_norm_similarity), int(is_outlier)
        ])

    # Write report CSV
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    # Print summary
    outliers = [r for r in rows[1:] if r[-1] == 1]
    print(f"\nSummary:")
    print(f"  Common files compared: {len(common)}")
    print(f"  Only in A (final_csv): {len(only_a)} -> {only_a[:5]}{'...' if len(only_a) > 5 else ''}")
    print(f"  Only in B (csv_data):  {len(only_b)} -> {only_b[:5]}{'...' if len(only_b) > 5 else ''}")
    print(f"  Outliers flagged:      {len(outliers)}")
    print(f"  Report written to:     {report_path}")

    if outliers:
        print("\nTop 10 outliers (by rel_size_diff then normalized similarity):")
        # filename idx0, rel_size idx4, sim idx12, norm sim idx13
        outliers_sorted = sorted(outliers, key=lambda r: (float(r[4]), 1 - float(r[13])), reverse=True)
        for r in outliers_sorted[:10]:
            print(f"  {r[0]} | rel_size={r[4]} sim={r[12]} norm_sim={r[13]} rows={r[5]}/{r[6]} sizes={r[1]}/{r[2]}")


if __name__ == "__main__":
    folder_a = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_A
    folder_b = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_B
    report = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_REPORT

    compare_folders(folder_a, folder_b, report)
