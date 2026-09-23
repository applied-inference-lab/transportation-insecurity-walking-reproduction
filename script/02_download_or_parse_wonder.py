"""02_download_or_parse_wonder.py

Downloads (if necessary) and harmonizes the CDC 2022 National Health Interview Survey (NHIS)
Sample Adult microdata for computational reproduction of Soto et al., PCD 2026;23:250436.

Applies survey inclusion criteria, mobility exclusions, and variable recoding.
Outputs:
- data/processed/nhis2022_adult_analytic.csv
- data/processed/sample_exclusion_cascade.csv
"""

import os
import urllib.request
import zipfile
import pandas as pd
import numpy as np

CDC_NHIS_URL = "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NHIS/2022/adult22csv.zip"
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

def download_and_extract():
    os.makedirs(RAW_DIR, exist_ok=True)
    csv_path = os.path.join(RAW_DIR, "adult22.csv")
    zip_path = os.path.join(RAW_DIR, "adult22csv.zip")
    
    if not os.path.exists(csv_path):
        if not os.path.exists(zip_path):
            print(f"Downloading {CDC_NHIS_URL}...")
            urllib.request.urlretrieve(CDC_NHIS_URL, zip_path)
            print("Download complete.")
        print(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(RAW_DIR)
        print("Extraction complete.")
    else:
        print(f"Found existing raw data file: {csv_path}")
    return csv_path

def parse_and_harmonize(csv_path):
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    cols = [
        "HHX", "URBRRL", "REGION", "PSTRAT", "PPSU", "WTFA_A",
        "SEX_A", "AGEP_A", "HISPALLP_A", "EDUCP_A", "DISAB3_A", "DIFF_A",
        "TRANSPOR_A", "WLKTRAN_A", "RATCAT_A", "POVRATTC_A"
    ]
    
    print("Reading CDC NHIS 2022 Adult dataset...")
    df = pd.read_csv(csv_path, usecols=cols, low_memory=False)
    n_initial = len(df)
    print(f"Initial sample size: {n_initial}")
    
    # 1. Exclusion: cannot walk at all or climb steps (DIFF_A == 4)
    # Question: "Are you able to walk or climb steps?" (4 = Cannot do at all)
    cannot_walk = (df["DIFF_A"] == 4)
    n_cannot_walk = cannot_walk.sum()
    df_step1 = df[~cannot_walk].copy()
    print(f"Excluded unable to walk/climb steps (DIFF_A == 4): {n_cannot_walk} -> Remaining: {len(df_step1)}")
    
    # 2. Exclusion: Missing transportation insecurity (TRANSPOR_A not in [1, 2])
    # 1 = Yes, 2 = No. 7=Refused, 8=Not Ascertained, 9=Don't Know.
    ti_valid = df_step1["TRANSPOR_A"].isin([1, 2])
    # Note: in sequential cascade, missing on TI:
    df_step2 = df_step1[ti_valid].copy()
    n_ti_excluded = len(df_step1) - len(df_step2)
    print(f"Excluded missing transportation insecurity: {n_ti_excluded} -> Remaining: {len(df_step2)}")
    
    # 3. Exclusion: Missing walking for transportation (WLKTRAN_A not in [1, 2])
    tw_valid = df_step2["WLKTRAN_A"].isin([1, 2])
    df_step3 = df_step2[tw_valid].copy()
    n_tw_excluded = len(df_step2) - len(df_step3)
    print(f"Excluded missing walking for transportation: {n_tw_excluded} -> Remaining: {len(df_step3)}")
    
    # 4. Exclusion: Missing sociodemographic or geographic characteristics
    demo_valid = (
        df_step3["SEX_A"].isin([1, 2]) &
        df_step3["AGEP_A"].between(18, 120) &
        df_step3["HISPALLP_A"].isin(range(1, 8)) &
        df_step3["EDUCP_A"].isin(range(1, 11)) &
        df_step3["DISAB3_A"].isin([1, 2]) &
        df_step3["REGION"].isin(range(1, 5)) &
        df_step3["URBRRL"].isin(range(1, 5)) &
        df_step3["RATCAT_A"].between(1, 14)
    )
    df_final = df_step3[demo_valid].copy()
    n_demo_excluded = len(df_step3) - len(df_final)
    print(f"Excluded missing sociodemographics: {n_demo_excluded} -> Final analytic sample: {len(df_final)}")
    
    # Record cascade
    cascade = pd.DataFrame([
        ("Total 2022 NHIS Sample Adults", n_initial, 0),
        ("Cannot walk at all or climb steps (DIFF_A == 4)", len(df_step1), n_cannot_walk),
        ("Missing transportation insecurity (TRANSPOR_A)", len(df_step2), n_ti_excluded),
        ("Missing walking for transportation (WLKTRAN_A)", len(df_step3), n_tw_excluded),
        ("Missing sociodemographic/geographic variables", len(df_final), n_demo_excluded),
    ], columns=["stage", "remaining_n", "excluded_n"])
    cascade.to_csv(os.path.join(PROCESSED_DIR, "sample_exclusion_cascade.csv"), index=False)
    
    # Harmonized Recodes
    # Sex
    df_final["sex"] = df_final["SEX_A"].map({1: "Male", 2: "Female"})
    
    # Age group
    age_bins = [17, 24, 34, 44, 64, 150]
    age_labels = ["18-24", "25-34", "35-44", "45-64", ">=65"]
    df_final["age_group"] = pd.cut(df_final["AGEP_A"], bins=age_bins, labels=age_labels)
    
    # Race and ethnicity (HISPALLP_A)
    # 1=Hispanic, 2=NH White, 3=NH Black, 4=NH Asian, 5=NH AIAN, 6=NH AIAN & any other, 7=NH Other/multi
    def recode_race(r):
        if r == 1:
            return "Hispanic or Latino/a"
        elif r == 2:
            return "Non-Hispanic White"
        elif r == 3:
            return "Non-Hispanic Black"
        elif r == 4:
            return "Non-Hispanic Asian"
        elif r in [5, 6]:
            return "Non-Hispanic AIAN"
        elif r == 7:
            return "Non-Hispanic Other/Multiple"
        return "Unknown"
    df_final["race_ethnicity"] = df_final["HISPALLP_A"].apply(recode_race)
    
    # Educational attainment (EDUCP_A)
    # 1,2: Less than high school
    # 3,4: High school or GED
    # 5,6,7: Some college or associate degree
    # 8,9,10: Bachelor degree or higher
    def recode_educ(e):
        if e in [1, 2]:
            return "Less than high school"
        elif e in [3, 4]:
            return "High school or GED"
        elif e in [5, 6, 7]:
            return "Some college or associate degree"
        elif e in [8, 9, 10]:
            return "Bachelor degree or higher"
        return "Unknown"
    df_final["education"] = df_final["EDUCP_A"].apply(recode_educ)
    
    # Disability status (DISAB3_A)
    # 1=With disability, 2=Without disability
    df_final["disability"] = df_final["DISAB3_A"].map({1: "With disabilities", 2: "Without disabilities"})
    
    # US Census region (REGION)
    # 1=Northeast, 2=Midwest, 3=South, 4=West
    df_final["region"] = df_final["REGION"].map({
        1: "Northeast", 2: "Midwest", 3: "South", 4: "West"
    })
    
    # Urban-rural classification (URBRRL)
    # 1=Large central metropolitan, 2=Large fringe metropolitan, 3=Medium and small metropolitan, 4=Nonmetropolitan
    df_final["urban_rural"] = df_final["URBRRL"].map({
        1: "Large central metropolitan",
        2: "Large fringe metropolitan",
        3: "Medium and small metropolitan",
        4: "Nonmetropolitan"
    })
    
    # Income-poverty ratio (RATCAT_A)
    # 1-3: <1.00; 4-7: 1.00-1.99; 8-9: 2.00-2.99; 10-11: 3.00-3.99; 12-14: >=4.00
    def recode_pov(p):
        if p in [1, 2, 3]:
            return "<1.00"
        elif p in [4, 5, 6, 7]:
            return "1.00-1.99"
        elif p in [8, 9]:
            return "2.00-2.99"
        elif p in [10, 11]:
            return "3.00-3.99"
        elif p in [12, 13, 14]:
            return ">=4.00"
        return "Unknown"
    df_final["poverty_ratio"] = df_final["RATCAT_A"].apply(recode_pov)
    
    # Binary outcomes: 1=Yes, 0=No
    df_final["trans_insecurity"] = (df_final["TRANSPOR_A"] == 1).astype(int)
    df_final["walk_trans"] = (df_final["WLKTRAN_A"] == 1).astype(int)
    
    out_csv = os.path.join(PROCESSED_DIR, "nhis2022_adult_analytic.csv")
    df_final.to_csv(out_csv, index=False)
    print(f"Saved harmonized dataset to {out_csv} with {len(df_final)} rows and {len(df_final.columns)} columns.")

if __name__ == "__main__":
    csv_file = download_and_extract()
    parse_and_harmonize(csv_file)
