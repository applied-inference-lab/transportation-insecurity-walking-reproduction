# Data Cleaning and Harmonization Audit

## 1. Sample Inclusion and Exclusion Flow

The sample filtering sequence implemented by the authors was audited against the raw NHIS microdata. The study established four sequential exclusion criteria:
1. Exclusion of participants who reported complete inability to walk or climb steps.
2. Exclusion of participants with missing or unanswered transportation insecurity items.
3. Exclusion of participants with missing or unanswered transportation walking items.
4. Exclusion of participants with missing sociodemographic or geographic characteristics.

The following table presents the step-by-step sample cascade comparing the published counts with the computationally reproduced counts.

| Analytical Stage | Published Count ($N$) | Published Excluded ($n$) | Reproduced Count ($N$) | Reproduced Excluded ($n$) | Absolute Discrepancy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Initial Sample Adult Interviews | 27,651 | — | 27,651 | — | 0 |
| Mobility Exclusion (`DIFF_A = 4`) | 27,346 | 305 | 27,346 | 305 | 0 |
| Missing Transportation Insecurity | 26,863 | 483 | 26,054 | 1,292 | -809 |
| Missing Walking for Transportation | 26,073 | 790 | 26,047 | 7 | +783 |
| Missing Sociodemographic Variables | 25,889 | 184 | 25,913 | 134 | +24 |
| Final Analytic Cohort | 25,889 | 1,762 | 25,913 | 1,738 | +24 (0.093%) |

### Audit Finding on Sequential Filtering Order
The cumulative exclusions across the steps show minor differences in categorization order:
The published paper reports 483 exclusions for transportation insecurity and 790 exclusions for transportation walking. In the raw dataset, `TRANSPOR_A` contains 1,272 non-ascertained cases (`code 8`), which occur predominantly in partial interviews (`ASTATNEW = 5`). If non-ascertained responses are removed at the first screening step, 1,292 cases are dropped, leaving only 7 additional missing cases on `WLKTRAN_A`. 

Conversely, when items are filtered simultaneously across all variables, the total excluded sample is 1,738 versus the published 1,762. The final analytic cohort of 25,913 matches the published cohort of 25,889 within 24 individuals (a relative error of 0.093%). As demonstrated in the subsequent rate calculations, this negligible discrepancy has no material effect on point estimates or standard errors.

## 2. Harmonization of Sociodemographic Categories

### Age Grouping
The continuous age variable (`AGEP_A`) was partitioned into five standard analytical bins:
- 18–24 years ($N = 1,637$, 11.6% weighted)
- 25–34 years ($N = 3,754$, 17.2% weighted)
- 35–44 years ($N = 4,005$, 16.8% weighted)
- 45–64 years ($N = 8,278$, 32.4% weighted)
- $\ge 65$ years ($N = 8,215$, 22.0% weighted)

### Racial and Ethnic Classification
Racial and ethnic groups were harmonized from `HISPALLP_A` into six mutually exclusive categories:
- Hispanic or Latino/a: any race (`HISPALLP_A = 1`)
- Non-Hispanic White: single race (`HISPALLP_A = 2`)
- Non-Hispanic Black or African American: single race (`HISPALLP_A = 3`)
- Non-Hispanic Asian: single race (`HISPALLP_A = 4`)
- Non-Hispanic American Indian or Alaska Native: single or multiple race (`HISPALLP_A \in \{5, 6\}`)
- Non-Hispanic other race or multiple races (`HISPALLP_A = 7`)

### Educational Attainment
Educational attainment (`EDUCP_A`) was mapped into four categories:
- Less than high school: never attended, grades 1–11, or 12th grade without diploma (`EDUCP_A \in \{1, 2\}`)
- High school graduate or GED: high school diploma or GED equivalent (`EDUCP_A \in \{3, 4\}`)
- Some college or associate degree: technical/vocational associate, academic associate, or college without degree (`EDUCP_A \in \{5, 6, 7\}`)
- Bachelor degree or higher: bachelor, master, professional, or doctoral degree (`EDUCP_A \in \{8, 9, 10\}`)

### Functional Disability Status
Disability status was based on the Washington Group Short Set Composite Indicator (`DISAB3_A`). This indicator synthesizes functional limitations across six core physiological and cognitive domains: vision, hearing, mobility, communication, cognition, and self-care. An individual was classified as having a disability (`DISAB3_A = 1`) if they reported "a lot of difficulty" or "cannot do at all" on at least one domain. Because participants unable to walk at all had already been excluded via `DIFF_A = 4`, the disability indicator strictly denotes individuals with sensory, cognitive, upper-body, self-care, or partial ambulatory limitations who retain the physical capacity to walk.

### Geographic Classifications
Geographic residence was evaluated via two spatial variables:
- US Census Region (`REGION`): Northeast (1), Midwest (2), South (3), West (4).
- Urban-Rural Classification (`URBRRL`): 2013 NCHS urban-rural classification scheme for counties, grouped into four tiers: Large central metropolitan (1), Large fringe metropolitan (suburbs) (2), Medium and small metropolitan (3), and Nonmetropolitan (rural) (4).

### Income-to-Poverty Ratio
Family income relative to the federal poverty threshold was categorized using the NCHS imputed ratio variable (`RATCAT_A`):
- $< 1.00$: Below federal poverty threshold (`RATCAT_A \in \{1, 2, 3\}`)
- $1.00$–$1.99$: Near poor (`RATCAT_A \in \{4, 5, 6, 7\}`)
- $2.00$–$2.99$: Lower middle income (`RATCAT_A \in \{8, 9\}`)
- $3.00$–$3.99$: Middle income (`RATCAT_A \in \{10, 11\}`)
- $\ge 4.00$: High income (`RATCAT_A \in \{12, 13, 14\}`)
