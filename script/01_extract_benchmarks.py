"""01_extract_benchmarks.py

Extracts published reference tables from Soto et al., PCD 2026;23:250436:
- Table 1: Prevalence of US adults with the ability to walk reporting transportation insecurity and transportation walking.
- Table 2: Prevalence of transportation walking among adults with and without transportation insecurity.

Saves structured reference benchmarks to data/benchmarks/.
"""

import os
import pandas as pd
import numpy as np

def extract_benchmarks():
    os.makedirs("data/benchmarks", exist_ok=True)
    
    # Table 1 Benchmarks
    t1_data = [
        # Domain, Category, Overall_N, Overall_Pct, TI_N, TI_Pct, TI_CI_low, TI_CI_high, TW_N, TW_Pct, TW_CI_low, TW_CI_high
        ("Overall", "Overall", 25889, 100.0, 1447, 5.6, 5.1, 6.2, 4073, 16.1, 15.4, 16.9),
        ("Sex", "Female", 14094, 51.3, 833, 6.0, 5.4, 6.6, 2038, 15.0, 14.1, 16.0),
        ("Sex", "Male", 11795, 48.7, 614, 5.3, 4.6, 5.9, 2035, 17.3, 16.3, 18.3),
        ("Age", "18-24", 1637, 11.6, 145, 8.5, 7.1, 10.1, 473, 27.7, 25.3, 30.2),
        ("Age", "25-34", 3754, 17.2, 230, 6.0, 5.0, 7.1, 833, 20.7, 19.1, 22.5),
        ("Age", "35-44", 4005, 16.8, 227, 5.7, 4.9, 6.7, 687, 16.3, 14.9, 17.7),
        ("Age", "45-64", 8278, 32.4, 463, 5.3, 4.6, 6.0, 1199, 13.3, 12.4, 14.3),
        ("Age", ">=65", 8215, 22.0, 382, 4.3, 3.8, 4.9, 881, 10.4, 9.5, 11.4),
        ("Race/Ethnicity", "Non-Hispanic AIAN", 346, 1.4, 47, 14.1, 9.0, 21.4, 62, 19.5, 14.6, 25.7),
        ("Race/Ethnicity", "Non-Hispanic Asian", 1555, 6.0, 57, 3.2, 2.4, 4.4, 334, 21.5, 18.9, 24.3),
        ("Race/Ethnicity", "Non-Hispanic Black", 2768, 11.3, 255, 9.1, 7.9, 10.4, 500, 18.6, 16.5, 20.9),
        ("Race/Ethnicity", "Hispanic or Latino/a", 3642, 17.0, 245, 6.8, 5.8, 8.0, 610, 16.5, 15.0, 18.1),
        ("Race/Ethnicity", "Non-Hispanic White", 17276, 62.9, 831, 4.7, 4.1, 5.4, 2489, 14.8, 13.9, 15.7),
        ("Race/Ethnicity", "Non-Hispanic Other/Multiple", 302, 1.4, np.nan, np.nan, np.nan, np.nan, 78, 25.9, 20.5, 32.0),
        ("Education", "Less than high school", 2152, 10.5, 219, 9.6, 8.2, 11.2, 352, 16.6, 14.8, 18.6),
        ("Education", "High school or GED", 6494, 26.9, 385, 6.1, 5.3, 6.9, 780, 13.2, 12.1, 14.4),
        ("Education", "Some college or associate degree", 7312, 29.6, 448, 5.9, 5.3, 6.7, 986, 14.8, 13.7, 15.9),
        ("Education", "Bachelor degree or higher", 9931, 33.0, 395, 3.7, 3.1, 4.5, 1955, 19.6, 18.4, 20.9),
        ("Disability", "With disabilities", 2416, 8.4, 346, 14.5, 12.6, 16.5, 260, 12.0, 10.4, 13.9),
        ("Disability", "Without disabilities", 23473, 91.6, 1101, 4.8, 4.3, 5.4, 3813, 16.5, 15.7, 17.3),
        ("Region", "Northeast", 4225, 17.3, 226, 4.9, 4.1, 5.9, 977, 25.1, 22.7, 27.8),
        ("Region", "Midwest", 5705, 20.9, 330, 6.4, 4.9, 8.3, 886, 16.4, 14.7, 18.2),
        ("Region", "South", 9478, 37.9, 522, 5.5, 4.9, 6.2, 989, 10.4, 9.4, 11.5),
        ("Region", "West", 6481, 23.8, 369, 5.8, 4.9, 6.7, 1221, 18.5, 16.9, 20.2),
        ("Urban-Rural", "Large central metropolitan", 7688, 30.7, 426, 5.7, 5.1, 6.5, 1871, 23.7, 22.0, 25.5),
        ("Urban-Rural", "Large fringe metropolitan", 6043, 25.2, 267, 4.7, 4.1, 5.4, 820, 14.2, 13.0, 15.6),
        ("Urban-Rural", "Medium and small metropolitan", 8087, 30.2, 516, 6.0, 4.9, 7.4, 997, 12.9, 11.8, 14.2),
        ("Urban-Rural", "Nonmetropolitan", 4071, 14.0, 238, 6.2, 4.9, 7.6, 385, 9.7, 8.4, 11.3),
        ("Income-Poverty Ratio", "<1.00", 2511, 9.4, 394, 15.6, 13.7, 17.6, 566, 24.0, 21.8, 26.3),
        ("Income-Poverty Ratio", "1.00-1.99", 4469, 17.6, 392, 9.2, 8.2, 10.3, 663, 16.3, 14.8, 17.9),
        ("Income-Poverty Ratio", "2.00-2.99", 4018, 16.1, 198, 5.0, 4.2, 6.0, 521, 13.2, 11.9, 14.6),
        ("Income-Poverty Ratio", "3.00-3.99", 3432, 12.9, 134, 3.8, 3.0, 4.8, 418, 12.2, 10.8, 13.7),
        ("Income-Poverty Ratio", ">=4.00", 11459, 44.1, 329, 2.9, 2.3, 3.5, 1905, 16.6, 15.6, 17.7),
    ]
    t1_cols = [
        "domain", "category", "overall_n", "overall_pct",
        "ti_n", "ti_pct", "ti_ci_low", "ti_ci_high",
        "tw_n", "tw_pct", "tw_ci_low", "tw_ci_high"
    ]
    df_t1 = pd.DataFrame(t1_data, columns=t1_cols)
    df_t1.to_csv("data/benchmarks/table1_benchmarks.csv", index=False)
    print("Saved data/benchmarks/table1_benchmarks.csv with", len(df_t1), "rows.")

    # Table 2 Benchmarks
    t2_data = [
        # Domain, Category, TI_Walk_N, TI_Walk_Pct, TI_Walk_CI_low, TI_Walk_CI_high, NonTI_Walk_N, NonTI_Walk_Pct, NonTI_Walk_CI_low, NonTI_Walk_CI_high
        ("Overall", "Overall", 417, 30.9, 27.9, 34.1, 3656, 15.3, 14.5, 16.1),
        ("Sex", "Female", 247, 33.2, 29.4, 37.3, 1791, 13.9, 13.0, 14.8),
        ("Sex", "Male", 170, 28.1, 23.8, 32.9, 1865, 16.7, 15.7, 17.7),
        ("Age", "18-24", 72, 47.9, 39.0, 57.0, 401, 25.8, 23.4, 28.4),
        ("Age", "25-34", 95, 40.7, 33.5, 48.4, 738, 19.5, 17.8, 21.2),
        ("Age", "35-44", 67, 29.3, 23.2, 36.3, 620, 15.5, 14.1, 16.9),
        ("Age", "45-64", 115, 23.4, 19.5, 27.8, 1084, 12.8, 11.8, 13.8),
        ("Age", ">=65", 68, 17.5, 13.0, 23.1, 813, 10.1, 9.2, 11.1),
        ("Race/Ethnicity", "Non-Hispanic AIAN", np.nan, np.nan, np.nan, np.nan, 46, 15.6, 11.5, 20.7),
        ("Race/Ethnicity", "Non-Hispanic Asian", np.nan, np.nan, np.nan, np.nan, 311, 20.8, 18.2, 23.7),
        ("Race/Ethnicity", "Non-Hispanic Black", 98, 42.6, 35.4, 50.2, 402, 16.2, 14.1, 18.6),
        ("Race/Ethnicity", "Hispanic or Latino/a", 75, 32.0, 25.7, 39.0, 535, 15.4, 13.9, 17.0),
        ("Race/Ethnicity", "Non-Hispanic White", 199, 24.5, 20.8, 28.5, 2290, 14.3, 13.4, 15.2),
        ("Race/Ethnicity", "Non-Hispanic Other/Multiple", np.nan, np.nan, np.nan, np.nan, 72, 24.5, 19.2, 30.7),
        ("Education", "Less than high school", 77, 38.8, 31.6, 46.5, 275, 14.3, 12.5, 16.2),
        ("Education", "High school or GED", 112, 31.0, 25.8, 36.7, 668, 12.1, 10.9, 13.3),
        ("Education", "Some college or associate degree", 119, 29.6, 24.8, 34.8, 867, 13.8, 12.8, 15.0),
        ("Education", "Bachelor degree or higher", 109, 26.4, 21.7, 31.6, 1846, 19.3, 18.1, 20.6),
        ("Disability", "With disabilities", 78, 25.3, 19.8, 31.6, 182, 9.8, 8.2, 11.6),
        ("Disability", "Without disabilities", 339, 32.5, 28.8, 36.3, 3474, 15.7, 14.9, 16.5),
        ("Region", "Northeast", 75, 34.9, 27.7, 42.8, 902, 24.6, 22.1, 27.3),
        ("Region", "Midwest", 92, 30.9, 24.3, 38.4, 794, 15.4, 13.8, 17.2),
        ("Region", "South", 117, 23.6, 19.3, 28.5, 872, 9.6, 8.7, 10.7),
        ("Region", "West", 133, 39.6, 34.0, 45.4, 1088, 17.2, 15.6, 18.9),
        ("Urban-Rural", "Large central metropolitan", 158, 36.0, 31.0, 41.3, 1713, 23.0, 21.2, 24.9),
        ("Urban-Rural", "Large fringe metropolitan", 73, 28.8, 22.7, 35.8, 747, 13.5, 12.3, 14.8),
        ("Urban-Rural", "Medium and small metropolitan", 136, 30.5, 25.0, 36.7, 861, 11.8, 10.7, 13.0),
        ("Urban-Rural", "Nonmetropolitan", 50, 24.1, 17.1, 32.9, 335, 8.8, 7.6, 10.2),
        ("Income-Poverty Ratio", "<1.00", 142, 39.8, 34.2, 45.7, 424, 21.1, 18.8, 23.5),
        ("Income-Poverty Ratio", "1.00-1.99", 111, 33.7, 28.3, 39.5, 552, 14.6, 13.1, 16.1),
        ("Income-Poverty Ratio", "2.00-2.99", 57, 29.4, 22.4, 37.5, 464, 12.3, 11.1, 13.7),
        ("Income-Poverty Ratio", "3.00-3.99", 33, 21.5, 13.7, 32.0, 385, 11.8, 10.4, 13.4),
        ("Income-Poverty Ratio", ">=4.00", 74, 21.7, 16.8, 27.6, 1831, 16.5, 15.4, 17.5),
    ]
    t2_cols = [
        "domain", "category",
        "ti_walk_n", "ti_walk_pct", "ti_walk_ci_low", "ti_walk_ci_high",
        "nonti_walk_n", "nonti_walk_pct", "nonti_walk_ci_low", "nonti_walk_ci_high"
    ]
    df_t2 = pd.DataFrame(t2_data, columns=t2_cols)
    df_t2.to_csv("data/benchmarks/table2_benchmarks.csv", index=False)
    print("Saved data/benchmarks/table2_benchmarks.csv with", len(df_t2), "rows.")

if __name__ == "__main__":
    extract_benchmarks()
