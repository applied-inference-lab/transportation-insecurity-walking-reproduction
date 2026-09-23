# Reproduction Protocol: Transportation Walking and Transportation Insecurity (NHIS 2022)

This document provides turnkey CLI execution instructions for independently reproducing all figures, tables, and audit metrics from raw CDC microdata.

## 1. Prerequisites and Setup

Ensure Python 3.12+ (or 3.14) is installed. Clone the repository and initialize the dedicated virtual environment:

```bash
# Navigate to the workspace repository root
cd 10.5888_pcd23.250436

# Initialize python virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install required dependencies
pip install -r reproduction/requirements.txt
```

*(Note: dependencies include `pandas>=3.0`, `numpy>=2.0`, `scipy>=1.18`, `statsmodels>=0.15`, `matplotlib>=3.11`, `seaborn>=0.13`, `pypdf>=6.19`, `openpyxl>=3.1`)*

## 2. End-to-End Pipeline Execution

Execute the modular analytical scripts sequentially. Each script performs fail-fast assertions and outputs structured CSV artifacts.

### Step 1: Benchmark Reference Extraction
Extracts published benchmarks from Table 1 and Table 2 in the paper PDF into structured reference CSVs.
```bash
python script/01_extract_benchmarks.py
```
*Outputs:*
- `data/benchmarks/table1_benchmarks.csv`
- `data/benchmarks/table2_benchmarks.csv`

### Step 2: Microdata Retrieval and Harmonization
Downloads the CDC NHIS 2022 Sample Adult public-use file (`adult22csv.zip`), extracts `adult22.csv`, applies eligibility filters (`DIFF_A != 4`), validates survey responses, and recodes sociodemographic variables.
```bash
python script/02_download_or_parse_wonder.py
```
*Outputs:*
- `data/raw/adult22.csv`
- `data/processed/nhis2022_adult_analytic.csv`
- `data/processed/sample_exclusion_cascade.csv`

### Step 3: Complex Survey Rate Computation and Audit
Computes survey-weighted proportions, Taylor Series Linearization standard errors, and logit-transformed 95% confidence intervals across all 33 demographic strata. Performs an automated discrepancy audit against published benchmarks.
```bash
python script/03_compute_rates.py
```
*Outputs:*
- `data/processed/table1_reproduced.csv`
- `data/processed/table2_reproduced.csv`
- `data/processed/table1_benchmark_audit.csv`
- `data/processed/table2_benchmark_audit.csv`
- `data/processed/reproduction_summary_metrics.json`

### Step 4: Statistical Testing and Multivariable Audit
Replicates Bonferroni-corrected pairwise survey $t$-tests and fits unadjusted and multivariable survey logistic regression models to evaluate residual confounding.
```bash
python script/04_run_trend_models.py
```
*Outputs:*
- `data/processed/pairwise_ttests_reproduced.csv`
- `data/processed/multivariable_logistic_models.csv`

### Step 5: Population Projections and Denominator Scaling
Translates sample proportions into nationwide population counts and constructs the side-by-side Absolute vs. Relative Risk comparison table.
```bash
python script/05_run_projections.py
```
*Outputs:*
- `data/processed/population_projections_and_audit.csv`
- `data/processed/absolute_vs_relative_risk.csv`

### Step 6: Publication-Grade Chart Generation
Renders replica and audit charts matching journal publication standards.
```bash
python script/06_plot_figures.py
```
*Outputs:*
- `documentation/figures/fig1_prevalence_comparison.png`
- `documentation/figures/fig2_absolute_vs_relative_risk.png`
- `documentation/figures/fig3_population_denominator_pyramid.png`
- `documentation/figures/fig4_benchmark_verification_audit.png`

## 3. Automated Validation and Pass/Fail Check

To verify reproduction integrity programmatically, inspect `data/processed/reproduction_summary_metrics.json`. The pipeline verifies that all prevalence estimates match published figures within 0.5 percentage points.
