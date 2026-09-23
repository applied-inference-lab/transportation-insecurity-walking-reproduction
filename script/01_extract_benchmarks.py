"""01_extract_benchmarks.py

Programmatically extracts published reference tables from the original CDC publication:
Soto et al., PCD 2026;23:250436 (DOI: 10.5888/pcd23.250436) via '25_0436.pdf'.
- Table 1: Prevalence of US adults with the ability to walk reporting transportation insecurity and transportation walking (pages 9-10).
- Table 2: Prevalence of transportation walking among adults with and without transportation insecurity (pages 11-12).

Parses PDF text streams dynamically using pypdf and regex, validates data schemas,
asserts extraction integrity, and saves structured reference CSVs to data/benchmarks/.
"""

import os
import re
import sys
import pypdf
import pandas as pd
import numpy as np


def clean_val(v):
    """Sanitizes extracted text tokens into float values, mapping suppressed symbols to NaN."""
    if v is None:
        return np.nan
    v = str(v).strip().replace(',', '')
    if v in ['', '-', '--', '-j', '-i', '—j', '—i', '—', '–']:
        return np.nan
    try:
        return float(v)
    except Exception:
        return np.nan


def extract_benchmarks_from_pdf(pdf_path="25_0436.pdf"):
    """Extracts Table 1 and Table 2 benchmarks programmatically from publication PDF."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Publication PDF not found at {pdf_path}")

    print(f"Opening {pdf_path} for programmatic table extraction...")
    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"Total pages in publication: {total_pages}")
    if total_pages < 12:
        raise ValueError(f"Expected at least 12 pages in publication PDF, found {total_pages}")

    # Standardized demographic domain & category sequence
    categories_seq = [
        ("Overall", "Overall"),
        ("Sex", "Female"),
        ("Sex", "Male"),
        ("Age", "18-24"),
        ("Age", "25-34"),
        ("Age", "35-44"),
        ("Age", "45-64"),
        ("Age", ">=65"),
        ("Race/Ethnicity", "Non-Hispanic AIAN"),
        ("Race/Ethnicity", "Non-Hispanic Asian"),
        ("Race/Ethnicity", "Non-Hispanic Black"),
        ("Race/Ethnicity", "Hispanic or Latino/a"),
        ("Race/Ethnicity", "Non-Hispanic White"),
        ("Race/Ethnicity", "Non-Hispanic Other/Multiple"),
        ("Education", "Less than high school"),
        ("Education", "High school or GED"),
        ("Education", "Some college or associate degree"),
        ("Education", "Bachelor degree or higher"),
        ("Disability", "With disabilities"),
        ("Disability", "Without disabilities"),
        ("Region", "Northeast"),
        ("Region", "Midwest"),
        ("Region", "South"),
        ("Region", "West"),
        ("Urban-Rural", "Large central metropolitan"),
        ("Urban-Rural", "Large fringe metropolitan"),
        ("Urban-Rural", "Medium and small metropolitan"),
        ("Urban-Rural", "Nonmetropolitan"),
        ("Income-Poverty Ratio", "<1.00"),
        ("Income-Poverty Ratio", "1.00-1.99"),
        ("Income-Poverty Ratio", "2.00-2.99"),
        ("Income-Poverty Ratio", "3.00-3.99"),
        ("Income-Poverty Ratio", ">=4.00"),
    ]

    # -------------------------------------------------------------
    # 1. TABLE 1 EXTRACTION (Pages 9 and 10 of PDF: 0-indexed 8, 9)
    # -------------------------------------------------------------
    print("Extracting Table 1 text stream from pages 9 and 10...")
    p9_text = reader.pages[8].extract_text()
    p10_text = reader.pages[9].extract_text()
    t1_full = (p9_text + "\n" + p10_text).replace("–", "-").replace("—", "-").replace("≥", ">=")

    # Table 1 row regex:
    # <overall_n> [(overall_pct)] <ti_n> <ti_pct> [(low-high)] <tw_n> <tw_pct> (low-high)
    t1_pattern = re.compile(
        r'([\d,]+)(?:\s*\(([\d.]+)\))?\s+'                    # overall_n, [overall_pct]
        r'([\d,]+|-j?|-i?)\s+'                               # ti_n or dash
        r'([\d.]+(?:\.\d+)?|-j?|-i?)\s*'                     # ti_pct or dash
        r'(?:\(([\d.]+)[-\s]+([\d.]+)\)[a-z,]*)?\s*'          # [ti_ci_low, ti_ci_high]
        r'([\d,]+)\s+'                                        # tw_n
        r'([\d.]+)\s*'                                        # tw_pct
        r'\(([\d.]+)[-\s]+([\d.]+)\)'                         # tw_ci_low, tw_ci_high
    )

    extracted_t1_rows = []
    for line in t1_full.splitlines():
        line = line.strip()
        m = t1_pattern.search(line)
        if m:
            g = m.groups()
            extracted_t1_rows.append([
                clean_val(g[0]), clean_val(g[1]),
                clean_val(g[2]), clean_val(g[3]), clean_val(g[4]), clean_val(g[5]),
                clean_val(g[6]), clean_val(g[7]), clean_val(g[8]), clean_val(g[9])
            ])

    if len(extracted_t1_rows) != 33:
        raise ValueError(f"Table 1 extraction error: Expected 33 rows, extracted {len(extracted_t1_rows)}")

    # Overall category percent is 100.0%
    extracted_t1_rows[0][1] = 100.0

    t1_data = []
    for i, (dom, cat) in enumerate(categories_seq):
        row = [dom, cat] + extracted_t1_rows[i]
        t1_data.append(row)

    t1_cols = [
        "domain", "category", "overall_n", "overall_pct",
        "ti_n", "ti_pct", "ti_ci_low", "ti_ci_high",
        "tw_n", "tw_pct", "tw_ci_low", "tw_ci_high"
    ]
    df_t1 = pd.DataFrame(t1_data, columns=t1_cols)

    # -------------------------------------------------------------
    # 2. TABLE 2 EXTRACTION (Pages 11 and 12 of PDF: 0-indexed 10, 11)
    # -------------------------------------------------------------
    print("Extracting Table 2 text stream from pages 11 and 12...")
    p11_text = reader.pages[10].extract_text()
    p12_text = reader.pages[11].extract_text()
    t2_full = (p11_text + "\n" + p12_text).replace("–", "-").replace("—", "-").replace("≥", ">=")

    # Table 2 row regex:
    # [ti_walk_n] [ti_walk_pct] [(ti_ci_low-ti_ci_high)] nonti_walk_n nonti_walk_pct (nonti_ci_low-nonti_ci_high)
    t2_pattern = re.compile(
        r'(?:([\d,]+)\s+([\d.]+)\s*\(([\d.]+)[-\s]+([\d.]+)\)[a-z,]*|(-i?|-j?)\s+(-i?|-j?))\s+' # TI walk
        r'([\d,]+)\s+([\d.]+)\s*\(([\d.]+)[-\s]+([\d.]+)\)'                                       # Non-TI walk
    )

    extracted_t2_rows = []
    for line in t2_full.splitlines():
        line = line.strip()
        m = t2_pattern.search(line)
        if m:
            g = m.groups()
            if g[4] is not None:  # Suppressed estimate (—i)
                ti_n, ti_pct, ti_low, ti_high = np.nan, np.nan, np.nan, np.nan
            else:
                ti_n, ti_pct, ti_low, ti_high = clean_val(g[0]), clean_val(g[1]), clean_val(g[2]), clean_val(g[3])
            non_n, non_pct, non_low, non_high = clean_val(g[6]), clean_val(g[7]), clean_val(g[8]), clean_val(g[9])
            extracted_t2_rows.append([ti_n, ti_pct, ti_low, ti_high, non_n, non_pct, non_low, non_high])

    if len(extracted_t2_rows) != 33:
        raise ValueError(f"Table 2 extraction error: Expected 33 rows, extracted {len(extracted_t2_rows)}")

    t2_data = []
    for i, (dom, cat) in enumerate(categories_seq):
        row = [dom, cat] + extracted_t2_rows[i]
        t2_data.append(row)

    t2_cols = [
        "domain", "category",
        "ti_walk_n", "ti_walk_pct", "ti_walk_ci_low", "ti_walk_ci_high",
        "nonti_walk_n", "nonti_walk_pct", "nonti_walk_ci_low", "nonti_walk_ci_high"
    ]
    df_t2 = pd.DataFrame(t2_data, columns=t2_cols)

    return df_t1, df_t2


def extract_benchmarks():
    """Extracts and saves structured reference benchmarks directly from 25_0436.pdf."""
    os.makedirs("data/benchmarks", exist_ok=True)
    pdf_path = "25_0436.pdf"

    df_t1, df_t2 = extract_benchmarks_from_pdf(pdf_path)

    # Save outputs
    out_t1 = "data/benchmarks/table1_benchmarks.csv"
    out_t2 = "data/benchmarks/table2_benchmarks.csv"

    df_t1.to_csv(out_t1, index=False)
    print(f"Saved {out_t1} ({len(df_t1)} rows extracted from pages 9-10).")

    df_t2.to_csv(out_t2, index=False)
    print(f"Saved {out_t2} ({len(df_t2)} rows extracted from pages 11-12).")

    # Assert integrity checks
    assert df_t1.loc[df_t1["category"] == "Overall", "overall_n"].values[0] == 25889
    assert df_t1.loc[df_t1["category"] == "Overall", "ti_pct"].values[0] == 5.6
    assert df_t1.loc[df_t1["category"] == "Overall", "tw_pct"].values[0] == 16.1
    assert df_t2.loc[df_t2["category"] == "Overall", "ti_walk_pct"].values[0] == 30.9
    assert df_t2.loc[df_t2["category"] == "Overall", "nonti_walk_pct"].values[0] == 15.3
    print("Verification assertions PASSED: All benchmark anchor values match publication exactly.")


if __name__ == "__main__":
    try:
        extract_benchmarks()
    except Exception as e:
        print(f"ERROR in benchmark extraction: {e}", file=sys.stderr)
        sys.exit(1)
