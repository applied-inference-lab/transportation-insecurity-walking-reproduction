# Population Projections and Denominator Scaling Audit

## 1. Nationwide Denominator Scaling

Epidemiological surveys that report percentage rates can inadvertently distort public health prioritization if fractional prevalences are not scaled to real-world population counts. In the 2022 NHIS analytic cohort, the survey sampling weights represent a civilian noninstitutionalized population of 238,327,048 American adults with the ability to walk.

The following table provides the nationwide population translations of the reported survey percentages.

| Population Parameter | Survey Proportion (%) | Weighted Population Count ($N$) | Share of Total Adults (%) | Share of All Walkers (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Target Adult Population** | 100.0% | 238,327,048 | 100.0% | — |
| **Transportation Secure Adults** | 94.37% | 224,898,465 | 94.37% | — |
| **Transportation Insecure Adults** | 5.63% | 13,428,583 | 5.63% | — |
| **Total Transportation Walkers** | 16.15% | 38,482,266 | 16.15% | 100.0% |
| **Transportation Insecure Walkers** | 30.92% (within TI) | 4,151,462 | 1.74% | 10.79% |
| **Transportation Secure Walkers** | 15.27% (within Secure) | 34,330,804 | 14.40% | 89.21% |

## 2. The Denominator Reality: The 89/11 Walker Split

The headline finding of the paper is that adults with transportation insecurity are twice as likely to walk for transportation as those without (30.9% versus 15.3%, a prevalence ratio of 2.03). 

However, translating these proportions to absolute counts reveals a critical structural asymmetry:
1. Because transportation insecurity is relatively uncommon (5.63% of adults), the overwhelming majority of people who walk for transportation in the United States—34,330,804 out of 38,482,266, or **89.21%**—are transportation secure.
2. In contrast, transportation-insecure walkers number 4,151,462 nationwide, representing just **1.74%** of the adult population and **10.79%** of all active transportation walkers.
3. This creates a public health paradox: while the risk ratio is doubled among insecure individuals, broad urban design interventions targeted solely where transportation insecurity is concentrated will miss almost 90% of all Americans who walk for transportation.

## 3. Counterfactual Scenario Simulations

To contextualize the public health leverage of targeted versus universal interventions, two counterfactual policy scenarios were simulated on the weighted microdata.

### Counterfactual Scenario A: Targeted Transit Subsidy / Vehicle Access
Assume a social welfare or transit policy successfully eliminates transportation insecurity, providing reliable personal vehicles or direct paratransit to all 13.4 million transportation-insecure adults. Under the assumption that these individuals then adopt the walking baseline of the transportation-secure population (falling from 30.92% to 15.27%):
- The number of transportation-insecure walkers decreases by $13,428,583 \times (0.3092 - 0.1527) = 2,101,573$ individuals.
- Total nationwide transportation walkers would decline from 38.5 million to 36.4 million (a net reduction of 5.46% in active transportation participants).
- While this intervention resolves transportation barriers and mobility frustration, it would paradoxically reduce total aerobic physical activity unless accompanied by leisure physical activity substitution.

### Counterfactual Scenario B: Universal Built-Environment Pedestrian Upgrades
Assume a nationwide pedestrian infrastructure initiative (curb cuts, protected crosswalks, sidewalk networks) achieves a modest 2.0 percentage point absolute increase in walking among the broader transportation-secure population (moving the rate from 15.27% to 17.27%):
- The gain in active transportation walkers would be $224,898,465 \times 0.020 = 4,497,969$ individuals.
- This single broad-based intervention creates more than twice the absolute number of walkers ($+4.50$ million) as the entire cohort of transportation-insecure walkers in existence nationwide ($4.15$ million).

### Policy Implication
These projections demonstrate that public health messaging must balance targeted equity interventions (protecting the 4.2 million necessity-driven walkers who face elevated pedestrian fatality risks in disinvested neighborhoods) with universal population-wide infrastructure investments (which drive macro-level cardiovascular health outcomes).
