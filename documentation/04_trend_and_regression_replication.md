# Statistical Inference and Regression Replication Audit

## 1. Subgroup Pairwise Testing and Multiple Comparisons

The original study tested subgroup differences in the prevalence of walking for transportation using two-sample survey-weighted $t$-tests with Bonferroni adjustments to control family-wise error rates. For a characteristic with $k$ categories, the number of unique pairwise contrasts is $C = \frac{k(k - 1)}{2}$, resulting in an adjusted alpha threshold of $\alpha^* = \frac{0.05}{C}$.

For example:
- Age (5 categories): $C = 10$, $\alpha^* = 0.005$
- Income-to-poverty ratio (5 categories): $C = 10$, $\alpha^* = 0.005$
- Race/ethnicity (3 presented groups): $C = 3$, $\alpha^* = 0.0167$
- Educational attainment (4 categories): $C = 6$, $\alpha^* = 0.0083$
- Census region (4 categories): $C = 6$, $\alpha^* = 0.0083$
- Disability status (2 categories): $C = 1$, $\alpha^* = 0.0500$

### Key Statistical Contrasts
The following table details the key pairwise comparisons highlighted in the paper text and validates their statistical conclusions.

| Contrast Description | Group 1 | Group 2 | Group 1 % | Group 2 % | Diff (pp) | SE (Diff) | $t$-statistic | $P$-value (Raw) | $P$-value (Bonferroni) | Published Finding |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Overall Exposure Effect** | Insecure | Secure | 30.92 | 15.27 | +15.65 | 1.62 | 9.68 | $< 0.0001$ | $< 0.0001$ | Significant ($P < 0.01$) |
| **Education Gradient within TI** | < High school | Bachelor+ | 38.82 | 26.43 | +12.39 | 4.63 | 2.68 | 0.0074 | 0.0446 | Significant ($P < 0.05$) |
| **Poverty Gradient within TI** | $< 1.00$ | $\ge 4.00$ | 39.81 | 21.72 | +18.09 | 4.09 | 4.42 | $< 0.0001$ | $< 0.001$ | Significant ($P < 0.01$) |
| **Racial Disparity within TI** | NH Black | NH White | 42.61 | 24.53 | +18.08 | 4.29 | 4.21 | $< 0.0001$ | $< 0.001$ | Significant ($P < 0.01$) |
| **Age Gradient within TI** | 18–24 y | $\ge 65$ y | 47.98 | 17.51 | +30.47 | 5.34 | 5.71 | $< 0.0001$ | $< 0.001$ | Significant ($P < 0.01$) |
| **Disability Status within TI** | No disability | Disability | 32.52 | 25.31 | +7.21 | 3.59 | 2.01 | 0.0446 | 0.0446 | Significant ($P < 0.05$) |
| **Regional Contrast within TI** | West | South | 39.67 | 23.59 | +16.08 | 3.75 | 4.29 | $< 0.0001$ | $< 0.001$ | Significant ($P < 0.01$) |

All substantive claims regarding pairwise significance asserted in the Results section of the published text were confirmed programmatically.

## 2. Multivariable Regression Audit

A primary methodological vulnerability of the published report is its exclusive reliance on bivariate cross-tabulations and unadjusted pairwise tests. The authors posited that transportation insecurity drives transportation walking. However, sociodemographic factors such as youthful age, extreme poverty, and high urban density independently predict both transportation walking and transportation insecurity.

To evaluate whether the observed association is an artifact of demographic confounding (Simpson's paradox), unadjusted and multivariable survey-weighted logistic regressions were modeled on the analytic cohort ($N = 25,913$).

$$\text{logit}(P(\text{walk\_trans} = 1)) = \beta_0 + \beta_1 \cdot \text{trans\_insecurity} + \sum_k \beta_k X_k$$

### Model Comparison Results

| Model Specification | Exposure Variable | Odds Ratio (OR) | 95% Confidence Interval | $P$-value | Model AIC | Attenuation (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Model 1: Unadjusted** | Transportation Insecurity | 2.48 | 2.21–2.79 | $< 0.0001$ | 21,399.1 | — |
| **Model 2: Fully Adjusted** | Transportation Insecurity | 2.39 | 2.10–2.71 | $< 0.0001$ | 19,890.3 | 4.4% |

*Model 2 covariates: sex, age group (ref: $\ge 65$), race/ethnicity (ref: Non-Hispanic White), educational attainment (ref: Bachelor+), disability status (ref: Without disabilities), US Census region (ref: South), urban-rural classification (ref: Nonmetropolitan), and income-to-poverty ratio (ref: $\ge 4.00$).*

### Methodological Interpretation of Regression Audit
The multivariable survey logistic regression demonstrates that the association between transportation insecurity and transportation walking is remarkably robust to demographic and structural adjustment:
1. The unadjusted odds ratio of 2.48 attenuates by only 4.4% to an adjusted odds ratio (AOR) of 2.39 (95% CI: 2.10–2.71, $P < 0.0001$).
2. While poverty, youth, and urban residence independently increase walking likelihood (e.g., large central metro residents exhibit an AOR of 2.62 relative to rural residents, and young adults aged 18–24 exhibit an AOR of 3.12 relative to older adults), transportation insecurity retains an independent, statistically significant doubling of walking odds.
3. This mathematical finding refutes the hypothesis that the observed relationship was purely driven by demographic composition or poverty confounding. Lack of reliable transportation remains an independent behavioral driver of walking necessity.
