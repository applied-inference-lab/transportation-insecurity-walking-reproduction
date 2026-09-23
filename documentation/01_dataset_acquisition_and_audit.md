# Dataset Acquisition and Survey Provenance Audit

## 1. Primary Source Identification

The target empirical investigation is:
Soto G, Van Dyke ME, Nakayama JY, Chen TJ, Devlin HM, Irani K, Matjasko JL, Zaganjor H, Whitfield GP. Transportation Walking Among US Adults With and Without Transportation Insecurity, 2022 National Health Interview Survey. *Preventing Chronic Disease* 2026;23:250436. DOI: 10.5888/pcd23.250436.

The underlying empirical microdata is drawn from the 2022 National Health Interview Survey (NHIS) Sample Adult component, released by the National Center for Health Statistics (NCHS) of the Centers for Disease Control and Prevention (CDC).

The survey represents the civilian noninstitutionalized population of the United States. In 2022, interviews were conducted continuously throughout the calendar year across all 50 states and the District of Columbia. Although historically administered via in-person household visits, pandemic disruptions led to 55.7% of the 2022 Sample Adult interviews being conducted partially or fully by telephone.

## 2. Source Data Retrieval and Integrity Verification

The dataset was obtained directly from the official CDC/NCHS FTP distribution repository. The file archive, checksums, and parameters are detailed in the following table.

| File Parameter | Value |
| :--- | :--- |
| Source URL | `https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NHIS/2022/adult22csv.zip` |
| Distribution Archive | `adult22csv.zip` (3,654,579 bytes) |
| Extracted Data File | `adult22.csv` (28,118,163 bytes) |
| Release Date | June 5, 2023 |
| Archive SHA256 | `25083298173ACFFF35C6635BE0FBCAA3FF26B985E0A48FC5E7D9788761864DBA` |
| CSV SHA256 | `2E814050EA06CA1FFED356F51979B87C20D6242B0453C928249A29BD5F1F29F1` |
| Total Raw Rows ($N$) | 27,651 |
| Total Variables ($P$) | 637 |

## 3. Data Dictionary of Analytical Variables

The analytical extraction utilized 16 distinct survey variables covering design stratification, primary sampling units, survey weighting, exposure assessment, primary outcome measurement, functional mobility, and sociodemographic characteristics.

| Variable Name | Survey Module | Variable Label in CDC Codebook | Analytical Coding Scheme |
| :--- | :--- | :--- | :--- |
| `HHX` | Identifier | Household number | Unique household cluster identifier |
| `PSTRAT` | Design | Pseudo-stratum for variance estimation | Stratification unit ($H = 300$ strata) |
| `PPSU` | Design | Pseudo-PSU for variance estimation | Primary sampling unit cluster |
| `WTFA_A` | Weight | Sample Adult final annual weight | Final probability sampling weight |
| `DIFF_A` | Functioning | Difficulty walking or climbing steps | 1=No difficulty, 2=Some, 3=A lot, 4=Cannot do at all, 7=Refused, 9=Don't know |
| `TRANSPOR_A` | Barrier | Lack of reliable transportation for daily living | 1=Yes, 2=No, 7=Refused, 8=Not ascertained, 9=Don't know |
| `WLKTRAN_A` | Walking | Walk for transportation, past 7 days | 1=Yes, 2=No, 7=Refused, 8=Not ascertained, 9=Don't know |
| `SEX_A` | Demographics | Sex of sample adult | 1=Male, 2=Female |
| `AGEP_A` | Demographics | Age of sample adult | Continuous years (18 to 85+) |
| `HISPALLP_A` | Demographics | Race/ethnicity with Hispanic origin | 1=Hispanic, 2=NH White, 3=NH Black, 4=NH Asian, 5/6=NH AIAN, 7=NH Other/Multi |
| `EDUCP_A` | Demographics | Educational attainment | 1-2=<High school, 3-4=High school/GED, 5-7=Some college, 8-10=Bachelor+ |
| `DISAB3_A` | Disability | Washington Group Short Set Composite | 1=With disability, 2=Without disability |
| `REGION` | Geography | US Census Region | 1=Northeast, 2=Midwest, 3=South, 4=West |
| `URBRRL` | Geography | 2013 NCHS urban-rural classification | 1=Large central, 2=Large fringe, 3=Medium/small metro, 4=Nonmetropolitan |
| `RATCAT_A` | Income | Ratio of family income to poverty threshold | 1-3=<1.00, 4-7=1.00-1.99, 8-9=2.00-2.99, 10-11=3.00-3.99, 12-14=>=4.00 |
| `POVRATTC_A` | Income | Top-coded continuous poverty ratio | Continuous ratio (0.00 to 11.00) |

## 4. Methodological Definition of Measures

### Transportation Insecurity
Transportation insecurity was evaluated through a single binary item in the Social Determinants of Health / Healthcare Access module (`TRANSPOR_A`). The question was posed as follows:
"In the past 12 months, has a lack of reliable transportation kept you from medical appointments, meetings, work, or from getting things you needed for daily living?"
Affirmative responses were coded as 1, while negative responses were coded as 0. All other responses (refused, not ascertained, don't know) were treated as missing.

### Transportation Walking
Walking for transportation was measured via the Physical Activity module item (`WLKTRAN_A`):
"In the past 7 days, did you walk to travel to and from work, to do errands, or to go from place to place?"
Respondents affirming the prompt were coded as 1, and those answering negatively were coded as 0.

### Eligibility Filter
The survey design incorporated an internal skip pattern: respondents reporting that they "cannot do at all" when asked about walking or climbing steps (`DIFF_A = 4`) were excluded by design from receiving the transportation walking questionnaire module. Consequently, all 305 individuals with complete inability to walk were excluded prior to sample derivation.

## 5. Audit of Source Integrity

The downloaded dataset was validated for byte counts and record totals against official NCHS documentation (`srvydesc-508.pdf` and `Adult-summary.pdf`). The unweighted total of 27,651 sample adults exactly matches the official CDC census of completed and partial Sample Adult interviews for survey year 2022.
