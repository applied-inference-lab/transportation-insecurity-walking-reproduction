# Computational Environment and Dependencies

## 1. System Architecture and Hardware

The computational reproduction was executed and verified on the following host environment:
- Operating System: Microsoft Windows 11 Enterprise (AMD64)
- Shell: PowerShell 7 / Windows PowerShell
- Python Runtime: Python 3.14.4 (64-bit)

## 2. Core Language and Package Dependencies

The analysis is contained within a dedicated virtual environment (`.venv`). Pinned library versions are documented below:

| Package | Version | Purpose |
| :--- | :--- | :--- |
| `pandas` | 3.0.6 | Data ingestion, survey filtering, aggregation, export |
| `numpy` | 2.5.3 | Array vectorization, matrix calculations |
| `scipy` | 1.18.1 | Statistical distributions, normal CDF calculations |
| `statsmodels` | 0.15.0 | Generalized Linear Models (survey-weighted logistic regression) |
| `matplotlib` | 3.11.2 | Vector and publication figure rendering |
| `seaborn` | 0.13.2 | Advanced visual aesthetics and barplot themes |
| `pypdf` | 6.19.0 | Automated PDF benchmark extraction and inspection |
| `openpyxl` | 3.1.5 | Excel spreadsheet interoperability |

## 3. Environment Replication Instructions

To reproduce the environment:
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r reproduction/requirements.txt
```
