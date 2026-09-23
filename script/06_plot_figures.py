"""06_plot_figures.py

Generates publication-grade figures for the computational reproduction and audit of
Soto et al., PCD 2026;23:250436:
- Figure 1: Walking Prevalence by Transportation Insecurity Status across Subgroups.
- Figure 2: Absolute vs. Relative Disparities (Relative Surge vs. Absolute Percentage Points).
- Figure 3: The Denominator Audit: Composition of US Transportation Walkers.
- Figure 4: Reproduction Benchmark Parity Plot (Published vs Reproduced Estimates).

Outputs PNG charts to documentation/figures/.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def set_style():
    plt.rcParams.update({
        'font.sans-serif': 'Arial',
        'font.family': 'sans-serif',
        'figure.dpi': 300,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 13
    })

def plot_fig1_prevalence_comparison():
    df_t2 = pd.read_csv("data/processed/table2_reproduced.csv")
    # Select representative key subgroups
    subgroups = [
        "Overall", "Female", "Male",
        "18-24", "45-64", ">=65",
        "Non-Hispanic Black", "Hispanic or Latino/a", "Non-Hispanic White",
        "Less than high school", "Bachelor degree or higher",
        "<1.00", ">=4.00",
        "Large central metropolitan", "Nonmetropolitan"
    ]
    df_plot = df_t2[df_t2["category"].isin(subgroups)].copy()
    # Sort order
    df_plot["order"] = df_plot["category"].apply(lambda x: subgroups.index(x))
    df_plot = df_plot.sort_values("order", ascending=False)
    
    y = np.arange(len(df_plot))
    height = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    rects1 = ax.barh(y + height/2, df_plot["ti_walk_pct"], height, label="With Transportation Insecurity", color="#b2182b", alpha=0.85)
    rects2 = ax.barh(y - height/2, df_plot["nonti_walk_pct"], height, label="Without Transportation Insecurity", color="#2166ac", alpha=0.85)
    
    # Add error bars
    ti_err = [
        df_plot["ti_walk_pct"] - df_plot["ti_walk_ci_low"],
        df_plot["ti_walk_ci_high"] - df_plot["ti_walk_pct"]
    ]
    nonti_err = [
        df_plot["nonti_walk_pct"] - df_plot["nonti_walk_ci_low"],
        df_plot["nonti_walk_ci_high"] - df_plot["nonti_walk_pct"]
    ]
    ax.errorbar(df_plot["ti_walk_pct"], y + height/2, xerr=ti_err, fmt='none', ecolor='black', capsize=2, alpha=0.7)
    ax.errorbar(df_plot["nonti_walk_pct"], y - height/2, xerr=nonti_err, fmt='none', ecolor='black', capsize=2, alpha=0.7)
    
    ax.set_yticks(y)
    ax.set_yticklabels(df_plot["category"])
    ax.set_xlabel("Prevalence of Transportation Walking (%, 95% CI)")
    ax.set_title("Figure 1. Prevalence of Transportation Walking by Insecurity Status", weight='bold', pad=15)
    ax.legend(loc="lower right", frameon=True)
    ax.set_xlim(0, 60)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    out_path = "documentation/figures/fig1_prevalence_comparison.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Saved {out_path}.")

def plot_fig2_absolute_vs_relative():
    df_risk = pd.read_csv("data/processed/absolute_vs_relative_risk.csv")
    subgroups = [
        "Overall", "Female", "Male",
        "18-24", "25-34", "35-44", "45-64", ">=65",
        "Non-Hispanic Black", "Hispanic or Latino/a", "Non-Hispanic White",
        "Less than high school", "High school or GED", "Some college or associate degree", "Bachelor degree or higher",
        "With disabilities", "Without disabilities",
        "Large central metropolitan", "Nonmetropolitan",
        "<1.00", "1.00-1.99", "2.00-2.99", "3.00-3.99", ">=4.00"
    ]
    df_plot = df_risk[df_risk["subgroup"].isin(subgroups)].copy()
    df_plot["order"] = df_plot["subgroup"].apply(lambda x: subgroups.index(x))
    df_plot = df_plot.sort_values("order")
    
    fig, ax1 = plt.subplots(figsize=(11, 7))
    
    color1 = '#2b83ba'
    color2 = '#d7191c'
    
    x = np.arange(len(df_plot))
    width = 0.4
    
    rects1 = ax1.bar(x - width/2, df_plot["relative_risk_ratio"], width, label="Relative Risk Ratio (Prevalence Ratio)", color=color1, alpha=0.85)
    ax1.set_ylabel("Relative Risk Ratio (Fold Increase)", color=color1, weight='bold')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(0, 3.5)
    ax1.axhline(1.0, color='gray', linestyle=':', alpha=0.7)
    
    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, df_plot["absolute_percentage_point_diff"], width, label="Absolute Percentage Point Difference", color=color2, alpha=0.85)
    ax2.set_ylabel("Absolute Difference (Percentage Points)", color=color2, weight='bold')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(0, 35)
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_plot["subgroup"], rotation=45, ha='right', fontsize=9)
    plt.title("Figure 2. Relative Risk Surge vs. Absolute Percentage Point Difference Across Subgroups", weight='bold', pad=15)
    
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    
    plt.tight_layout()
    out_path = "documentation/figures/fig2_absolute_vs_relative_risk.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Saved {out_path}.")

def plot_fig3_denominator_audit():
    df_pop = pd.read_csv("data/processed/population_projections_and_audit.csv")
    pop_ti_w = df_pop.loc[df_pop["metric"] == "Transportation Walkers who are Transportation Insecure", "count"].values[0] / 1e6
    pop_nonti_w = df_pop.loc[df_pop["metric"] == "Transportation Walkers who are Transportation Secure", "count"].values[0] / 1e6
    pop_ti_nowalk = (df_pop.loc[df_pop["metric"] == "Transportation Insecure Population", "count"].values[0] - pop_ti_w * 1e6) / 1e6
    pop_nonti_nowalk = (df_pop.loc[df_pop["metric"] == "Transportation Secure Population", "count"].values[0] - pop_nonti_w * 1e6) / 1e6
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Subplot 1: Total Adult Population by Insecurity Status
    sizes1 = [pop_nonti_nowalk + pop_nonti_w, pop_ti_nowalk + pop_ti_w]
    labels1 = [f'Transportation Secure\n224.9M (94.4%)', f'Transportation Insecure\n13.4M (5.6%)']
    colors1 = ['#4575b4', '#d73027']
    ax1.pie(sizes1, labels=labels1, colors=colors1, autopct='%1.1f%%', startangle=140, explode=(0, 0.1), textprops={'fontsize': 10})
    ax1.set_title("A. Total US Adult Population\n(N = 238.3 Million)", weight='bold')
    
    # Subplot 2: Transportation Walkers Breakdown
    sizes2 = [pop_nonti_w, pop_ti_w]
    labels2 = [f'Secure Walkers\n34.3M (89.2%)', f'Insecure Walkers\n4.2M (10.8%)']
    colors2 = ['#74add1', '#f46d43']
    ax2.pie(sizes2, labels=labels2, colors=colors2, autopct='%1.1f%%', startangle=140, explode=(0, 0.1), textprops={'fontsize': 10})
    ax2.set_title("B. US Transportation Walkers\n(N = 38.5 Million Walkers)", weight='bold')
    
    plt.suptitle("Figure 3. The Denominator Reality: 89.2% of All Transportation Walkers are Transportation Secure", weight='bold', y=1.02)
    plt.tight_layout()
    out_path = "documentation/figures/fig3_population_denominator_pyramid.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Saved {out_path}.")

def plot_fig4_benchmark_parity():
    a1 = pd.read_csv("data/processed/table1_benchmark_audit.csv")
    a2 = pd.read_csv("data/processed/table2_benchmark_audit.csv")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Panel A: Table 1 Prevalences
    t1_valid_ti = a1.dropna(subset=["ti_pct_rep", "ti_pct_pub"])
    t1_valid_tw = a1.dropna(subset=["tw_pct_rep", "tw_pct_pub"])
    
    ax1.scatter(t1_valid_ti["ti_pct_pub"], t1_valid_ti["ti_pct_rep"], color='#d73027', alpha=0.75, s=40, label="Transportation Insecurity %")
    ax1.scatter(t1_valid_tw["tw_pct_pub"], t1_valid_tw["tw_pct_rep"], color='#4575b4', alpha=0.75, s=40, marker='^', label="Transportation Walking %")
    ax1.plot([0, 35], [0, 35], color='black', linestyle='--', alpha=0.5, label='1:1 Line')
    ax1.set_xlabel("Published Prevalence (%)")
    ax1.set_ylabel("Reproduced Prevalence (%)")
    ax1.set_title("A. Table 1 Estimates (33 Strata)", weight='bold')
    ax1.legend(loc="upper left")
    ax1.grid(True, linestyle=':', alpha=0.5)
    
    # Panel B: Table 2 Prevalences
    t2_valid_ti = a2.dropna(subset=["ti_walk_pct_rep", "ti_walk_pct_pub"])
    t2_valid_nonti = a2.dropna(subset=["nonti_walk_pct_rep", "nonti_walk_pct_pub"])
    
    ax2.scatter(t2_valid_ti["ti_walk_pct_pub"], t2_valid_ti["ti_walk_pct_rep"], color='#d73027', alpha=0.75, s=40, label="Walk % Among Insecure")
    ax2.scatter(t2_valid_nonti["nonti_walk_pct_pub"], t2_valid_nonti["nonti_walk_pct_rep"], color='#4575b4', alpha=0.75, s=40, marker='s', label="Walk % Among Secure")
    ax2.plot([0, 55], [0, 55], color='black', linestyle='--', alpha=0.5, label='1:1 Line')
    ax2.set_xlabel("Published Prevalence (%)")
    ax2.set_ylabel("Reproduced Prevalence (%)")
    ax2.set_title("B. Table 2 Estimates (33 Strata)", weight='bold')
    ax2.legend(loc="upper left")
    ax2.grid(True, linestyle=':', alpha=0.5)
    
    plt.suptitle("Figure 4. Computational Reproduction Parity Plots: Published vs. Reproduced Estimates", weight='bold', y=1.02)
    plt.tight_layout()
    out_path = "documentation/figures/fig4_benchmark_verification_audit.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Saved {out_path}.")

if __name__ == "__main__":
    set_style()
    plot_fig1_prevalence_comparison()
    plot_fig2_absolute_vs_relative()
    plot_fig3_denominator_audit()
    plot_fig4_benchmark_parity()
