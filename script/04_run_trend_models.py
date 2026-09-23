"""04_run_trend_models.py

Executes the statistical inference models for Soto et al., PCD 2026;23:250436:
1. Replicates the survey pairwise t-tests with Bonferroni adjustments across demographic subgroups.
2. Performs the critical methodological audit regression:
   - Unadjusted survey logistic regression (walk_trans ~ trans_insecurity)
   - Multivariable survey logistic regression adjusting for age, sex, race/ethnicity,
     education, disability, region, urbanicity, and income-to-poverty ratio.
   - Evaluates whether the "doubling" of walking among transportation insecure individuals
     is an artifact of demographic composition and structural poverty (Simpson's paradox / confounding).

Outputs:
- data/processed/pairwise_ttests_reproduced.csv
- data/processed/multivariable_logistic_models.csv
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

def compute_domain_mean_var(df, y_col, mask):
    """Computes survey weighted mean and Taylor linearization variance for a subpopulation."""
    sub = df[mask].copy()
    if len(sub) == 0:
        return 0, 0, 0
    w = sub["WTFA_A"].values
    y = sub[y_col].values
    N_hat = np.sum(w)
    p_hat = np.sum(w * y) / N_hat
    sub["_z"] = w * (y - p_hat)
    psu_sums = sub.groupby(["PSTRAT", "PPSU"])["_z"].sum().reset_index()
    var_total = 0.0
    for strat, group in psu_sums.groupby("PSTRAT"):
        n_h = len(group)
        if n_h > 1:
            z_hi = group["_z"].values
            z_h_bar = np.mean(z_hi)
            var_total += (n_h / (n_h - 1)) * np.sum((z_hi - z_h_bar) ** 2)
    var_p = var_total / (N_hat ** 2)
    return p_hat, np.sqrt(var_p), var_p

def run_pairwise_tests(df):
    results = []
    
    # 1. Test walking prevalence between TI vs Non-TI overall
    p_ti, se_ti, var_ti = compute_domain_mean_var(df, "walk_trans", df["trans_insecurity"] == 1)
    p_nonti, se_nonti, var_nonti = compute_domain_mean_var(df, "walk_trans", df["trans_insecurity"] == 0)
    diff = p_ti - p_nonti
    se_diff = np.sqrt(var_ti + var_nonti)
    t_stat = diff / se_diff
    p_val = 2 * (1 - stats.norm.cdf(abs(t_stat)))
    results.append({
        "comparison_type": "TI vs Non-TI Overall",
        "group1": "Transportation Insecure",
        "group2": "Transportation Secure",
        "p1_pct": round(p_ti * 100, 2),
        "p2_pct": round(p_nonti * 100, 2),
        "diff_pct": round(diff * 100, 2),
        "se_diff_pct": round(se_diff * 100, 2),
        "t_statistic": round(t_stat, 3),
        "raw_p_value": p_val,
        "bonferroni_p_value": p_val,
        "significant_05": p_val < 0.05
    })
    
    # 2. Key subgroup comparisons among adults with transportation insecurity highlighted in paper:
    # - Lowest vs highest educational attainment: Less than high school vs Bachelor degree+
    mask_ti = (df["trans_insecurity"] == 1)
    p_low_ed, se_low_ed, v_low_ed = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["education"] == "Less than high school"))
    p_hi_ed, se_hi_ed, v_hi_ed = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["education"] == "Bachelor degree or higher"))
    d_ed = p_low_ed - p_hi_ed
    se_d_ed = np.sqrt(v_low_ed + v_hi_ed)
    t_ed = d_ed / se_d_ed
    p_ed = 2 * (1 - stats.norm.cdf(abs(t_ed)))
    # Education has 4 categories -> 6 comparisons -> Bonferroni threshold 0.05/6 = 0.0083
    results.append({
        "comparison_type": "Within TI: Education",
        "group1": "Less than high school",
        "group2": "Bachelor degree or higher",
        "p1_pct": round(p_low_ed * 100, 2),
        "p2_pct": round(p_hi_ed * 100, 2),
        "diff_pct": round(d_ed * 100, 2),
        "se_diff_pct": round(se_d_ed * 100, 2),
        "t_statistic": round(t_ed, 3),
        "raw_p_value": p_ed,
        "bonferroni_p_value": min(1.0, p_ed * 6),
        "significant_05": p_ed < (0.05 / 6)
    })
    
    # - Below vs above poverty: <1.00 vs >=4.00
    p_pov_low, _, v_pov_low = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["poverty_ratio"] == "<1.00"))
    p_pov_hi, _, v_pov_hi = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["poverty_ratio"] == ">=4.00"))
    d_pov = p_pov_low - p_pov_hi
    se_d_pov = np.sqrt(v_pov_low + v_pov_hi)
    t_pov = d_pov / se_d_pov
    p_pov = 2 * (1 - stats.norm.cdf(abs(t_pov)))
    # Poverty has 5 categories -> 10 comparisons
    results.append({
        "comparison_type": "Within TI: Poverty Ratio",
        "group1": "<1.00 Poverty Threshold",
        "group2": ">=4.00 Poverty Threshold",
        "p1_pct": round(p_pov_low * 100, 2),
        "p2_pct": round(p_pov_hi * 100, 2),
        "diff_pct": round(d_pov * 100, 2),
        "se_diff_pct": round(se_d_pov * 100, 2),
        "t_statistic": round(t_pov, 3),
        "raw_p_value": p_pov,
        "bonferroni_p_value": min(1.0, p_pov * 10),
        "significant_05": p_pov < (0.05 / 10)
    })
    
    # - Non-Hispanic Black vs Non-Hispanic White
    p_blk, _, v_blk = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["race_ethnicity"] == "Non-Hispanic Black"))
    p_wht, _, v_wht = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["race_ethnicity"] == "Non-Hispanic White"))
    d_race = p_blk - p_wht
    se_d_race = np.sqrt(v_blk + v_wht)
    t_race = d_race / se_d_race
    p_race = 2 * (1 - stats.norm.cdf(abs(t_race)))
    # Tested between presented 3 groups (Black, Hispanic, White) -> 3 comparisons
    results.append({
        "comparison_type": "Within TI: Race/Ethnicity",
        "group1": "Non-Hispanic Black",
        "group2": "Non-Hispanic White",
        "p1_pct": round(p_blk * 100, 2),
        "p2_pct": round(p_wht * 100, 2),
        "diff_pct": round(d_race * 100, 2),
        "se_diff_pct": round(se_d_race * 100, 2),
        "t_statistic": round(t_race, 3),
        "raw_p_value": p_race,
        "bonferroni_p_value": min(1.0, p_race * 3),
        "significant_05": p_race < (0.05 / 3)
    })
    
    # - Age 18-24 vs >=65
    p_young, _, v_young = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["age_group"] == "18-24"))
    p_old, _, v_old = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["age_group"] == ">=65"))
    d_age = p_young - p_old
    se_d_age = np.sqrt(v_young + v_old)
    t_age = d_age / se_d_age
    p_age = 2 * (1 - stats.norm.cdf(abs(t_age)))
    # Age has 5 categories -> 10 comparisons
    results.append({
        "comparison_type": "Within TI: Age",
        "group1": "18-24 years",
        "group2": ">=65 years",
        "p1_pct": round(p_young * 100, 2),
        "p2_pct": round(p_old * 100, 2),
        "diff_pct": round(d_age * 100, 2),
        "se_diff_pct": round(se_d_age * 100, 2),
        "t_statistic": round(t_age, 3),
        "raw_p_value": p_age,
        "bonferroni_p_value": min(1.0, p_age * 10),
        "significant_05": p_age < (0.05 / 10)
    })
    
    # - Without disabilities vs With disabilities
    p_nodis, _, v_nodis = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["disability"] == "Without disabilities"))
    p_dis, _, v_dis = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["disability"] == "With disabilities"))
    d_dis = p_nodis - p_dis
    se_d_dis = np.sqrt(v_nodis + v_dis)
    t_dis = d_dis / se_d_dis
    p_dis_val = 2 * (1 - stats.norm.cdf(abs(t_dis)))
    results.append({
        "comparison_type": "Within TI: Disability",
        "group1": "Without disabilities",
        "group2": "With disabilities",
        "p1_pct": round(p_nodis * 100, 2),
        "p2_pct": round(p_dis * 100, 2),
        "diff_pct": round(d_dis * 100, 2),
        "se_diff_pct": round(se_d_dis * 100, 2),
        "t_statistic": round(t_dis, 3),
        "raw_p_value": p_dis_val,
        "bonferroni_p_value": p_dis_val,
        "significant_05": p_dis_val < 0.05
    })
    
    # - West vs South
    p_west, _, v_west = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["region"] == "West"))
    p_south, _, v_south = compute_domain_mean_var(df, "walk_trans", mask_ti & (df["region"] == "South"))
    d_reg = p_west - p_south
    se_d_reg = np.sqrt(v_west + v_south)
    t_reg = d_reg / se_d_reg
    p_reg = 2 * (1 - stats.norm.cdf(abs(t_reg)))
    # Region has 4 categories -> 6 comparisons
    results.append({
        "comparison_type": "Within TI: Region",
        "group1": "West",
        "group2": "South",
        "p1_pct": round(p_west * 100, 2),
        "p2_pct": round(p_south * 100, 2),
        "diff_pct": round(d_reg * 100, 2),
        "se_diff_pct": round(se_d_reg * 100, 2),
        "t_statistic": round(t_reg, 3),
        "raw_p_value": p_reg,
        "bonferroni_p_value": min(1.0, p_reg * 6),
        "significant_05": p_reg < (0.05 / 6)
    })

    df_ttests = pd.DataFrame(results)
    df_ttests.to_csv("data/processed/pairwise_ttests_reproduced.csv", index=False)
    print("Saved data/processed/pairwise_ttests_reproduced.csv.")

def run_multivariable_audit(df):
    """
    Fits unadjusted and multivariable survey-weighted logistic regressions:
    Outcome: walk_trans
    Model 1: walk_trans ~ trans_insecurity (Unadjusted)
    Model 2: walk_trans ~ trans_insecurity + sex + age_group + race_ethnicity + education + disability + region + urban_rural + poverty_ratio (Fully Adjusted)
    """
    # Normalize weights so sum equals sample size for GLM fitting
    df_reg = df.copy()
    w_norm = df_reg["WTFA_A"] * (len(df_reg) / df_reg["WTFA_A"].sum())
    
    # Model 1: Unadjusted
    m1 = smf.glm(
        "walk_trans ~ trans_insecurity",
        data=df_reg,
        family=sm.families.Binomial(),
        freq_weights=w_norm
    ).fit()
    
    or_unadj = np.exp(m1.params["trans_insecurity"])
    ci_unadj_low = np.exp(m1.conf_int().loc["trans_insecurity", 0])
    ci_unadj_high = np.exp(m1.conf_int().loc["trans_insecurity", 1])
    p_unadj = m1.pvalues["trans_insecurity"]
    
    # Model 2: Fully Adjusted
    formula_adj = (
        "walk_trans ~ trans_insecurity + C(sex, Treatment('Male')) + "
        "C(age_group, Treatment('>=65')) + "
        "C(race_ethnicity, Treatment('Non-Hispanic White')) + "
        "C(education, Treatment('Bachelor degree or higher')) + "
        "C(disability, Treatment('Without disabilities')) + "
        "C(region, Treatment('South')) + "
        "C(urban_rural, Treatment('Nonmetropolitan')) + "
        "C(poverty_ratio, Treatment('>=4.00'))"
    )
    m2 = smf.glm(
        formula_adj,
        data=df_reg,
        family=sm.families.Binomial(),
        freq_weights=w_norm
    ).fit()
    
    or_adj = np.exp(m2.params["trans_insecurity"])
    ci_adj_low = np.exp(m2.conf_int().loc["trans_insecurity", 0])
    ci_adj_high = np.exp(m2.conf_int().loc["trans_insecurity", 1])
    p_adj = m2.pvalues["trans_insecurity"]
    
    # Attenuation calculation
    # log(OR_unadj) vs log(OR_adj)
    pct_attenuation = (m1.params["trans_insecurity"] - m2.params["trans_insecurity"]) / m1.params["trans_insecurity"] * 100.0
    
    model_records = [
        {
            "model": "Model 1: Unadjusted",
            "predictor": "Transportation Insecurity",
            "odds_ratio": round(or_unadj, 3),
            "ci_95_low": round(ci_unadj_low, 3),
            "ci_95_high": round(ci_unadj_high, 3),
            "p_value": p_unadj,
            "aic": round(m1.aic, 1),
            "attenuation_pct": 0.0
        },
        {
            "model": "Model 2: Multivariable Adjusted",
            "predictor": "Transportation Insecurity",
            "odds_ratio": round(or_adj, 3),
            "ci_95_low": round(ci_adj_low, 3),
            "ci_95_high": round(ci_adj_high, 3),
            "p_value": p_adj,
            "aic": round(m2.aic, 1),
            "attenuation_pct": round(pct_attenuation, 1)
        }
    ]
    df_models = pd.DataFrame(model_records)
    df_models.to_csv("data/processed/multivariable_logistic_models.csv", index=False)
    print("Saved data/processed/multivariable_logistic_models.csv.")
    print(f"Unadjusted OR: {or_unadj:.2f} ({ci_unadj_low:.2f}-{ci_unadj_high:.2f})")
    print(f"Adjusted OR: {or_adj:.2f} ({ci_adj_low:.2f}-{ci_adj_high:.2f}), Attenuation: {pct_attenuation:.1f}%")

if __name__ == "__main__":
    analytic_path = "data/processed/nhis2022_adult_analytic.csv"
    df = pd.read_csv(analytic_path)
    run_pairwise_tests(df)
    run_multivariable_audit(df)
