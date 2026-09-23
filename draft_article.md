# Walking by Choice Versus Walking by Necessity: A Computational Reproduction and Methodological Audit of Transportation Insecurity and Active Travel in the 2022 National Health Interview Survey

**Author**: James Pusateri  
**Affiliation**: Middle Coast Software Inc.  
**Correspondence**: james.pusateri@middlecoastsoftware.com  

---

## Abstract

**Introduction**: Physical activity surveillance often treats walking as an unalloyed positive health behavior. A recent investigation by Soto and colleagues (Preventing Chronic Disease 2026;23:250436) analyzed the 2022 National Health Interview Survey (NHIS) and reported that adults experiencing transportation insecurity were twice as likely to walk for transportation as those without insecurity (30.9% vs. 15.3%). This study executes a computational reproduction of the published benchmarks, audits the statistical methodology, and provides population-level context.

**Methods**: Microdata from the 2022 NHIS Sample Adult interview ($N = 27,651$) was processed following the authors' filtering criteria, yielding an analytic sample of 25,913 ambulatory adults (a 0.093% difference from the published 25,889 cohort). Proportions, Taylor Series Linearization standard errors, and logit-transformed 95% confidence intervals were estimated across 33 demographic strata. Pairwise survey $t$-tests with Bonferroni adjustments were reproduced, and multivariable survey logistic regression was conducted to assess residual confounding. Proportions were scaled to the 238.3 million civilian noninstitutionalized adult population.

**Results**: The computational reproduction achieved exact parity across all 66 published proportion benchmarks, with a maximum discrepancy of $\le 0.1$ percentage points. The headline prevalence ratio was confirmed at 2.02 (30.9% vs. 15.3%, $P < 0.0001$), reflecting an absolute difference of 15.6 percentage points. In multivariable survey logistic regression, the association was attenuated by only 4.4% after adjusting for age, sex, race/ethnicity, education, disability, region, urbanicity, and income-to-poverty ratio (unadjusted OR: 2.48, 95% CI: 2.21–2.79; adjusted OR: 2.39, 95% CI: 2.10–2.71). Population-level scaling revealed that because transportation insecurity affects only 5.63% of adults (13.4 million), 89.2% of all active transportation walkers in the United States (34.3 million out of 38.5 million) are transportation secure. Transportation-insecure walkers represent just 1.74% of the adult population. A qualitative inversion of the socioeconomic gradient was uncovered: among secure adults, college graduates walk more than high school dropouts (19.3% vs. 14.3%), whereas among insecure adults, high school dropouts walk far more than college graduates (38.8% vs. 26.4%).

**Conclusion**: The findings of Soto et al. are computationally reproducible. However, the exclusive focus on relative risk ratios obscures two critical structural realities. First, broad pedestrian infrastructure cannot rely on transportation insecurity indicators alone without bypassing nine out of ten transportation walkers. Second, the observed physical activity among transportation-insecure minorities represents compelled walking under hostile pedestrian conditions rather than elective leisure activity.

---

## Introduction

Aerobic physical activity is a foundational pillar of chronic disease prevention, with regular walking associated with substantial reductions in cardiovascular mortality, type 2 diabetes incidence, and cognitive decline (US Department of Health and Human Services, 2018). Within physical activity surveillance, walking for transportation—defined as walking to travel to and from work, run errands, or reach transit destinations—is frequently promoted as an accessible, cost-effective mechanism for accumulating daily active minutes (Whitfield et al., 2018).

In a recent study published in *Preventing Chronic Disease*, Soto and colleagues (2026) evaluated the intersection of transportation insecurity and transportation walking using the 2022 National Health Interview Survey (NHIS). The authors defined transportation insecurity as the lack of safe, convenient, and reliable transportation for daily living and medical appointments. Analyzing a cross-sectional cohort of 25,889 adults with the ability to walk, the authors reported that adults with transportation insecurity were twice as likely to walk for transportation (30.9%; 95% CI: 27.9%–34.1%) as adults without transportation insecurity (15.3%; 95% CI: 14.5%–16.1%). Based on these findings, the authors concluded that walking for transportation may serve as an underused source of physical activity and recommended prioritizing pedestrian infrastructure in communities experiencing high transportation insecurity.

While the empirical association reported by Soto et al. draws attention to transportation equity, relying on unadjusted cross-tabulations and headline relative risk ratios introduces potential interpretive risks. First, the paper did not report multivariable-adjusted models, leaving open the possibility that the doubling of walking prevalence was confounded by age, extreme poverty, or urban density. Second, relative risk ratios can exaggerate public health impact when the underlying exposure prevalence is low. Third, the study did not disaggregate walking by choice from walking by necessity, which carries distinct implications for injury risk.

This investigation performs a formal computational reproduction of Soto et al. (2026), evaluates the numerical accuracy of the published tables against raw CDC microdata, and executes a critical methodological audit examining denominator scaling, absolute risk, residual confounding, and socioeconomic gradient inversions.

---

## Methods

### Data Source and Study Population
The primary data source was the 2022 NHIS Sample Adult public-use microdata file (`adult22.csv`), distributed by the National Center for Health Statistics (NCHS). The NHIS is a continuous, multistage probability sample of the civilian noninstitutionalized US population.

Following the published protocol, participants were included if they completed the Sample Adult interview and were ambulatory. Participants who reported complete inability to walk or climb steps (`DIFF_A = 4`, $n = 305$) were excluded because they were ineligible for the transportation walking assessment. In accordance with complete-case reporting, participants missing data on transportation insecurity (`TRANSPOR_A`, $n = 1,292$), walking for transportation (`WLKTRAN_A`, $n = 7$), or sociodemographic/geographic covariates ($n = 134$) were excluded, yielding a final analytic cohort of $N = 25,913$ individuals.

### Variable Definitions
1. **Transportation Insecurity**: Assessed via the binary question: "In the past 12 months, has a lack of reliable transportation kept you from medical appointments, meetings, work, or from getting things you needed for daily living?" Affirmative responses were coded as exposed (`TRANSPOR_A = 1`), and negative responses as unexposed (`TRANSPOR_A = 2`).
2. **Transportation Walking**: Assessed via the question: "In the past 7 days, did you walk to travel to and from work, to do errands, or to go from place to place?" Coded as binary (`WLKTRAN_A = 1` vs. `2`).
3. **Sociodemographic Covariates**: Categorized into sex (Female, Male); age groups (18–24, 25–34, 35–44, 45–64, $\ge 65$ years); race and ethnicity (Non-Hispanic AIAN, Non-Hispanic Asian, Non-Hispanic Black, Hispanic or Latino/a, Non-Hispanic White, Non-Hispanic Other/Multiple); educational attainment (< High school, High school/GED, Some college/AA, Bachelor degree+); functional disability (Washington Group Short Set 6-domain composite indicator `DISAB3_A`); US Census region (Northeast, Midwest, South, West); 2013 NCHS urban-rural classification (Large central metro, Large fringe metro, Medium/small metro, Nonmetropolitan); and family income-to-poverty ratio (`RATCAT_A`: $<1.00$, $1.00$–$1.99$, $2.00$–$2.99$, $3.00$–$3.99$, $\ge 4.00$).

### Statistical Analysis and Variance Estimation
To account for the complex survey design, point estimates were weighted using the final Sample Adult probability weight (`WTFA_A`). Standard errors were computed using first-order Taylor Series Linearization based on the 300 pseudo-strata (`PSTRAT`) and pseudo-PSUs (`PPSU`). Asymmetric 95% confidence intervals were generated via logit transformations in accordance with NCHS data presentation guidelines.

Pairwise two-sided survey $t$-tests with Bonferroni corrections were replicated for all subgroup comparisons. To evaluate potential confounding, survey-weighted multivariable logistic regression models were estimated, regressing transportation walking onto transportation insecurity while adjusting for sex, age group, race/ethnicity, educational attainment, disability status, census region, urbanicity, and income-to-poverty ratio.

Survey estimates were scaled to the nationwide adult population using the sum of survey weights ($\hat{N} = 238,327,048$). Absolute risk differences (ARR) and Number Needed to Observe (NNO) metrics were calculated across all strata. Computations were executed in Python 3.14 using `pandas`, `numpy`, `scipy`, and `statsmodels`.

---

## Results

### Benchmark Verification and Numerical Parity
The derived analytic sample of 25,913 adults matched the published cohort of 25,889 within 24 individuals, representing a relative discrepancy of 0.093%. 

Computational reproduction of the 33 strata in Table 1 and the 33 strata in Table 2 demonstrated complete numerical alignment:
- Overall prevalence of transportation insecurity was reproduced at 5.63% (95% CI: 5.14%–6.16%), exactly matching the published 5.6% (95% CI: 5.1%–6.2%).
- Overall prevalence of transportation walking was reproduced at 16.15% (95% CI: 15.42%–16.91%), exactly matching the published 16.1% (95% CI: 15.4%–16.9%).
- Walking prevalence among adults with transportation insecurity was reproduced at 30.92% (95% CI: 27.94%–34.05%), matching the published 30.9% (95% CI: 27.9%–34.1%).
- Walking prevalence among adults without transportation insecurity was reproduced at 15.27% (95% CI: 14.49%–16.08%), matching the published 15.3% (95% CI: 14.5%–16.1%).
- Across all 66 proportion benchmarks, the maximum absolute difference was $\le 0.1$ percentage points, confirming full computational reproduction (**Figure 4**).

### Multivariable Confounding Audit
In unadjusted survey logistic regression, adults experiencing transportation insecurity exhibited 2.48 times higher odds of walking for transportation (OR: 2.48; 95% CI: 2.21–2.79; $P < 0.0001$). 

After simultaneous multivariable adjustment for sex, age group, race/ethnicity, educational attainment, disability status, region, urban-rural classification, and poverty ratio, the adjusted odds ratio was 2.39 (95% CI: 2.10–2.71; $P < 0.0001$). Covariate adjustment produced an attenuation of only 4.4%. While urban residence (AOR: 2.62 for large central metro vs. rural) and younger age (AOR: 3.12 for ages 18–24 vs. $\ge 65$) were strong independent predictors of walking, transportation insecurity remained an independent determinant of active travel.

### Absolute Risk and the Denominator Split
Translating survey proportions into nationwide population counts revealed a pronounced denominator asymmetry. The 2022 survey represents 238,327,048 ambulatory adults. Within this population:
- 13,428,583 adults (5.63%) experience transportation insecurity.
- 38,482,266 adults (16.15%) walk for transportation.
- Among active transportation walkers, 34,330,804 individuals (89.21%) are transportation secure, while 4,151,462 individuals (10.79%) are transportation insecure (**Figure 3**).
- Transportation-insecure walkers represent just 1.74% of the entire US adult population.

Contrasting the headline relative risk against absolute measures demonstrated that the 2.02-fold relative increase corresponds to an absolute prevalence difference of 15.65 percentage points. Across subgroups, the absolute difference ranged from +5.2 percentage points among high-income adults ($\ge 4.00$ poverty threshold) to +26.4 percentage points among Non-Hispanic Black adults (**Figure 2**). The overall Number Needed to Observe was 6.4 individuals.

### Structural Inversion of Socioeconomic Gradients
Stratified analysis demonstrated a profound interaction between socioeconomic status and walking prevalence. Among transportation-secure adults, walking prevalence increased with education: college graduates walked at a rate of 19.3%, whereas adults without a high school diploma walked at 14.3%. 

Among adults with transportation insecurity, this gradient inverted: adults with less than a high school education exhibited a walking prevalence of 38.8%, compared to 26.4% among college graduates. A parallel inversion occurred across poverty tiers: among the secure, high-income adults walked at 16.5% compared to 12.3% among middle-income peers. Among the insecure, the lowest poverty tier walked at 39.8%, falling monotonically to 21.7% in the highest tier.

---

## Critical Methodological Audit

This audit evaluates the substantive methodology of Soto et al. against epidemiological standards for surveillance studies.

### 1. The Denominator Asymmetry and Resource Misallocation
The paper emphasized that walking was twice as common among transportation-insecure adults, leading to recommendations that infrastructure investments be prioritized where transportation insecurity is high. However, scaling to the national denominator demonstrates that nearly 90% of all transportation walkers in the United States do not experience transportation insecurity. Prioritizing pedestrian improvements solely through the lens of transportation insecurity programs risks bypassing 34.3 million active walkers. A balanced public health framework requires universal pedestrian infrastructure paired with targeted interventions in high-hazard corridors.

### 2. Confounding vs. Structural Compulsion
The authors did not fit multivariable models, which risked leaving the reported doubling vulnerable to claims of demographic confounding. Our multivariable audit confirmed that the effect is not a statistical artifact: the AOR remains 2.39 ($P < 0.0001$). However, the persistence of this effect underscores that transportation insecurity functions as a structural constraint. Individuals without access to personal vehicles or reliable transit walk not as an elective leisure choice, but as an unavoidable survival mechanism to access employment, groceries, and medical appointments.

### 3. Walking by Choice Versus Walking by Necessity
The qualitative inversion of educational and poverty gradients uncovered in our reanalysis illustrates the dual nature of walking in America. For higher-income, educated adults, walking is largely elective, occurring in walkable neighborhoods with high destination density. For low-income and minority adults experiencing transportation insecurity, walking is compelled. Compelled walking frequently occurs in hostile built environments characterized by multi-lane arterials, missing sidewalks, and high vehicular speeds. 

National pedestrian crash data confirms that pedestrian fatalities are heavily concentrated in low-income and minority communities. Smart Growth America (2024) reported that Black pedestrians are struck and killed at rates 82% higher than White pedestrians. Celebrating high walking prevalence among transportation-insecure Black adults (42.6%) without addressing roadside danger conflates exposure to environmental hazards with health promotion.

### 4. Temporal Mismatch in Measurement Instruments
A methodological limitation of the NHIS survey design is temporal dissonance between exposure and outcome. Transportation insecurity was assessed over the preceding 12 months, whereas transportation walking was assessed over the past 7 days. A respondent who faced acute vehicle failure eight months prior but currently has access to a vehicle is classified as transportation insecure, while their walking behavior reflects current circumstances. This exposure misclassification tends to bias effect estimates toward the null, suggesting that the true immediate impact of transit deprivation on walking may be even more acute.

### 5. Single-Item Screening Instrument Sensitivity
The single-item NHIS surveillance question identified a transportation insecurity prevalence of 5.6%. In contrast, comprehensive validated instruments, such as the 16-item Transportation Security Index (TSI) utilized by Murphy et al. (2022), estimate national prevalence at 24.0%. The NHIS question captures only severe material disruption (missing medical care or work), omitting moderate relational and logistical distress. Consequently, the cohort analyzed by Soto et al. represents an acutely deprived subpopulation, which explains their high rate of compelled walking.

---

## Discussion

The computational reproduction confirms the numerical integrity of Soto et al. (2026). The complex survey weighting, Taylor series variance estimation, and Bonferroni adjustments are technically sound and replicate published benchmarks within 0.1 percentage points.

However, forensic audit of the epidemiological framing reveals that headline relative risks can distort public health reality. When a risk ratio of 2.02 is interpreted in isolation, it implies that transportation insecurity is the primary locus of active travel in the United States. In reality, transportation-insecure walkers represent only 1.74% of the US adult population, and 89.2% of all walkers are transportation secure. 

Furthermore, public health surveillance must distinguish between elective and compelled physical activity. Promoting transportation walking as an unreserved health benefit among transportation-insecure populations ignores the reality of environmental injustice. When individuals walk because they lack a reliable vehicle, they are frequently forced onto infrastructure designed exclusively for high-speed automobile transit. Infrastructure investments in these communities must not merely encourage walking; they must provide physical separation, signalized crossings, and traffic calming to prevent pedestrian trauma.

---

## Conflict of Interest and Funding

The author declares no financial conflicts of interest. The author is affiliated with Middle Coast Software Inc., which is developing a software product to facilitate automated computational reproduction of published scientific literature. No external funding, grants, or commercial support were received for this study.
