"""05_run_projections.py

Executes population-level projections and real-world denominator scaling:
1. Translates survey rates into nationwide adult population counts using NHIS 2022 weights.
2. Constructs the side-by-side Absolute vs. Relative Risk audit table.
3. Simulates counterfactual policy interventions (e.g., providing reliable vehicle/transit
   access to transportation-insecure adults vs. broad-based pedestrian infrastructure expansion).

Outputs:
- data/processed/population_projections_and_audit.csv
- data/processed/absolute_vs_relative_risk.csv
"""

import os
import pandas as pd
import numpy as np

def run_projections():
    analytic_path = "data/processed/nhis2022_adult_analytic.csv"
    if not os.path.exists(analytic_path):
        raise FileNotFoundError(f"Missing {analytic_path}.")
        
    df = pd.read_csv(analytic_path)
    
    # Total weighted population represented
    total_pop = df["WTFA_A"].sum()
    
    # Stratum populations
    df_ti = df[df["trans_insecurity"] == 1]
    df_nonti = df[df["trans_insecurity"] == 0]
    
    pop_ti = df_ti["WTFA_A"].sum()
    pop_nonti = df_nonti["WTFA_A"].sum()
    
    # Walker populations
    df_walk = df[df["walk_trans"] == 1]
    pop_walk = df_walk["WTFA_A"].sum()
    
    walk_ti = df_ti[df_ti["walk_trans"] == 1]["WTFA_A"].sum()
    walk_nonti = df_nonti[df_nonti["walk_trans"] == 1]["WTFA_A"].sum()
    
    # Rates
    rate_ti = pop_ti / total_pop
    rate_nonti = pop_nonti / total_pop
    rate_walk = pop_walk / total_pop
    
    walk_rate_ti = walk_ti / pop_ti
    walk_rate_nonti = walk_nonti / pop_nonti
    
    # Risk Metrics
    rr = walk_rate_ti / walk_rate_nonti
    arr = walk_rate_ti - walk_rate_nonti
    nnt_equivalent = 1.0 / arr
    
    # Share of walkers that are transportation insecure
    share_walkers_ti = walk_ti / pop_walk
    share_walkers_nonti = walk_nonti / pop_walk
    
    # Total population share of TI walkers
    pop_share_ti_walk = walk_ti / total_pop
    
    # Counterfactual Scenarios:
    # Scenario A: "Eliminating Insecurity" -> TI adults adopt Non-TI walking rate (15.27%)
    # Delta walkers: pop_ti * (walk_rate_ti - walk_rate_nonti)
    scenario_a_delta = pop_ti * (walk_rate_ti - walk_rate_nonti)
    
    # Scenario B: "Universal Walkability" -> 2 percentage point increase in walking among Non-TI adults
    scenario_b_delta = pop_nonti * 0.02
    
    # Build Population Breakdown Table
    pop_records = [
        {"metric": "Total Civilian Noninstitutionalized Adult Population", "count": int(total_pop), "pct_of_total": 100.0},
        {"metric": "Transportation Insecure Population", "count": int(pop_ti), "pct_of_total": round(rate_ti * 100, 2)},
        {"metric": "Transportation Secure Population", "count": int(pop_nonti), "pct_of_total": round(rate_nonti * 100, 2)},
        {"metric": "Total Transportation Walkers in US", "count": int(pop_walk), "pct_of_total": round(rate_walk * 100, 2)},
        {"metric": "Transportation Walkers who are Transportation Insecure", "count": int(walk_ti), "pct_of_total": round(pop_share_ti_walk * 100, 2)},
        {"metric": "Transportation Walkers who are Transportation Secure", "count": int(walk_nonti), "pct_of_total": round((walk_nonti / total_pop) * 100, 2)},
        {"metric": "Share of All Walkers who are Transportation Insecure", "count": int(walk_ti), "pct_of_total": round(share_walkers_ti * 100, 2)},
        {"metric": "Share of All Walkers who are Transportation Secure", "count": int(walk_nonti), "pct_of_total": round(share_walkers_nonti * 100, 2)},
        {"metric": "Counterfactual A: Walker reduction if TI given vehicles/transit", "count": int(-scenario_a_delta), "pct_of_total": round((-scenario_a_delta / pop_walk) * 100, 2)},
        {"metric": "Counterfactual B: Walker gain from +2% walking in secure population", "count": int(scenario_b_delta), "pct_of_total": round((scenario_b_delta / pop_walk) * 100, 2)},
    ]
    df_pop = pd.DataFrame(pop_records)
    df_pop.to_csv("data/processed/population_projections_and_audit.csv", index=False)
    print("Saved data/processed/population_projections_and_audit.csv.")
    
    # Build Absolute vs Relative Risk Table by Subgroup
    t2 = pd.read_csv("data/processed/table2_reproduced.csv")
    risk_records = []
    for _, row in t2.iterrows():
        p_ti = row["ti_walk_pct"]
        p_nonti = row["nonti_walk_pct"]
        if pd.isna(p_ti) or pd.isna(p_nonti):
            continue
        rel_risk = p_ti / p_nonti
        abs_diff = p_ti - p_nonti
        nnt_equiv = round(100.0 / abs_diff, 1) if abs_diff > 0 else np.nan
        risk_records.append({
            "domain": row["domain"],
            "subgroup": row["category"],
            "ti_walking_pct": p_ti,
            "nonti_walking_pct": p_nonti,
            "relative_risk_ratio": round(rel_risk, 2),
            "relative_percent_increase": round((rel_risk - 1.0) * 100.0, 1),
            "absolute_percentage_point_diff": round(abs_diff, 1),
            "number_needed_for_one_additional_walker": nnt_equiv
        })
    df_risk = pd.DataFrame(risk_records)
    df_risk.to_csv("data/processed/absolute_vs_relative_risk.csv", index=False)
    print("Saved data/processed/absolute_vs_relative_risk.csv.")
    
    print("\n=== POPULATION DENOMINATOR AUDIT ===")
    print(f"Total US Adult Pop Represented: {total_pop:,.0f}")
    print(f"Transportation Insecure: {pop_ti:,.0f} ({rate_ti*100:.2f}%)")
    print(f"Total Transportation Walkers: {pop_walk:,.0f} ({rate_walk*100:.2f}%)")
    print(f"TI Walkers: {walk_ti:,.0f} ({share_walkers_ti*100:.1f}% of all walkers, {pop_share_ti_walk*100:.2f}% of US adults)")
    print(f"Secure Walkers: {walk_nonti:,.0f} ({share_walkers_nonti*100:.1f}% of all walkers)")
    print(f"Headline Relative Risk: {rr:.2f}x vs Absolute Difference: {arr*100:.2f} percentage points")

if __name__ == "__main__":
    run_projections()
