# When Walking Is Not a Choice: Auditing the CDC Study on Transportation Insecurity

**Author**: James Pusateri  
**Affiliation**: Middle Coast Software Inc.  
**Contact**: james.pusateri@middlecoastsoftware.com  

---

## The Headline Claim Versus the Raw Numbers

A recent study published by researchers from the Centers for Disease Control and Prevention in *Preventing Chronic Disease*, titled [Transportation Walking Among US Adults With and Without Transportation Insecurity, 2022 National Health Interview Survey](https://doi.org/10.5888/pcd23.250436), reported a striking headline: American adults who suffer from transportation insecurity are twice as likely to walk for transportation as those with reliable transit access. 

The report, authored by Graycie Soto and colleagues, analyzed data from 25,889 participants in the 2022 National Health Interview Survey. According to the published estimates, 30.9% of transportation-insecure adults walked for travel or errands in the past week, compared to only 15.3% of adults without transportation insecurity. The authors framed these findings as an encouraging sign that active travel represents an underused source of cardiovascular physical activity, arguing that municipal leaders should prioritize walking infrastructure where transportation insecurity is concentrated.

The study has been reproduced from the raw CDC microdata, and the published mathematics are verified as exact. Weighted estimates match the published tables down to a single decimal place across all 33 demographic strata.

Yet behind the headline ratio of 2.02 lies a very different real-world distribution. When fractional percentages are translated into national population counts, the data reveals that almost nine out of ten transportation walkers in the United States have no transportation insecurity whatsoever. Furthermore, a closer examination of the data uncovers an uncomfortable divide between walking as an elective health behavior and walking as a dangerous daily necessity.

---

## An Exemplary Reproduction: Why This Is a Success, Not a Failure

Before examining the interpretive traps inherent in headline relative risk metrics, it is essential to establish the forensic baseline: this study is a mathematical success.

In scientific auditing, investigations typically fall into one of two categories. The first category consists of analytical failures: studies compromised by transcription errors, miscalculated sampling weights, selective data exclusions, or spurious associations that collapse the moment a multivariable model is introduced. In such cases, the appropriate path is adversarial, requiring formal letters to the editor, errata, or retractions through official journal channels.

The second category consists of studies whose empirical calculations are airtight, but whose headline narrative requires critical context and epidemiological translation. The work of Soto et al. stands as a prime example of the latter.

When audited against the CDC's 2022 raw microdata, the published numbers held up with remarkable precision:
- The analytic sample derivation ($N = 25,913$ versus the published 25,889) was reproduced within 24 individuals, a relative discrepancy of less than a tenth of one percent.
- All 66 published prevalence estimates across Table 1 and Table 2 aligned within $\le 0.1$ percentage points using complex survey weighting and Taylor Series Linearization across 300 geographical strata.
- Crucially, when an unadjusted survey logistic regression model was subjected to full multivariable adjustment—controlling simultaneously for age, sex, race and ethnicity, educational attainment, functional disability, census region, county-level urbanicity, and family income-to-poverty ratios—the association did not disappear. The unadjusted odds ratio of 2.48 attenuated by only 4.4% to an adjusted odds ratio of 2.39 (95% CI: 2.10–2.71, $P < 0.0001$). The authors did not fall into a demographic confounding trap; transportation insecurity remains an authentic, independent driver of active travel.

Because the published mathematics are sound, there is no need for an official journal correction. The purpose of this audit is not to throw stones at well-executed descriptive surveillance, but to provide the structural context, denominator scaling, and policy nuance that an isolated headline ratio of 2.02 leaves out.

---

## The Denominator Problem: The 89/11 Split

In public health communication, relative risk ratios frequently create an optical illusion. Telling healthcare leaders that a group is twice as likely to engage in a behavior naturally leads them to assume that this group constitutes the core of that behavior.

To understand why this is misleading, consider the national denominator. The 2022 survey weights represent roughly 238.3 million civilian American adults who have the physical ability to walk. 

Here is how the numbers actually break down across the country:

1. **Transportation Insecurity Is a Niche Exposure**: Only 5.63% of American adults—about 13.4 million people—report experiencing transportation insecurity under the survey's definition. The remaining 94.37% (224.9 million adults) have reliable transportation.
2. **Transportation Walkers Total 38.5 Million**: Nationwide, 16.15% of adults reported walking to work, running errands, or traveling on foot during the prior seven days.
3. **The Vast Majority of Walkers Are Transportation Secure**: Of those 38.5 million active transportation walkers, 34.3 million (89.2%) have reliable transportation. Only 4.2 million walkers (10.8%) experience transportation insecurity.
4. **The Population Share**: Relative to the entire adult population of the United States, transportation-insecure walkers represent just 1.74%.

This distinction carries immediate consequences for municipal planners and healthcare executives. If a city designs pedestrian transit policies based primarily on maps of transportation insecurity, it will target its investments toward an important group of 4.2 million individuals, but it will completely bypass the 34.3 million Americans who account for nine-tenths of all pedestrian travel.

---

## Relative Surges Versus Absolute Differences

The study emphasized that transportation-insecure adults are twice as likely to walk. Translating this headline into absolute risk clarifies the clinical reality.

The absolute difference between a 30.9% walking rate and a 15.3% walking rate is 15.6 percentage points. In clinical epidemiology, this translates to a Number Needed to Observe (NNO) of 6.4. That is, an observer would need to interview between six and seven adults experiencing transportation insecurity to find one additional regular transportation walker compared to the secure population.

When stratified across sociodemographic tiers, the absolute differences diverge substantially:
- Among adults with annual incomes four or more times the federal poverty threshold, the absolute difference in walking between the insecure and secure is only 5.2 percentage points (21.7% vs. 16.5%).
- Among Non-Hispanic Black adults, the absolute difference expands to 26.4 percentage points (42.6% vs. 16.2%).
- Among young adults aged 18 to 24, the absolute difference reaches 22.1 percentage points (47.9% vs. 25.8%).

A high relative risk ratio can conceal small absolute differences in low-risk cohorts while obscuring acute absolute concentrations in disadvantaged groups.

---

## The Educational Inversion: Choice Versus Necessity

The most revealing pattern in the microdata is one that the original study acknowledged only briefly: the complete inversion of the socioeconomic gradient between transportation-secure and transportation-insecure Americans.

Consider educational attainment:
- Among adults **with reliable transportation**, walking for travel increases with education. College graduates walk at a rate of 19.3%, while those without a high school diploma walk at 14.3%.
- Among adults **without reliable transportation**, this pattern completely reverses. College graduates walk at a rate of 26.4%, while those without a high school diploma walk at 38.8%.

A parallel inversion occurs across income levels:
- In the transportation-secure population, the highest income tier ($\ge 4.00$ times the poverty threshold) walks at 16.5%, noticeably higher than the middle-income tiers (11.8% to 12.3%).
- In the transportation-insecure population, the poorest adults ($< 1.00$ poverty threshold) walk at 39.8%, falling steadily to 21.7% in the top tier.

These numbers document two fundamentally different activities that happen to share the same English word:

1. **Walking by Choice**: Higher-income, college-educated urban professionals walking through dense, pedestrian-friendly neighborhoods to grab lunch or commute from a subway station. This is elective physical activity.
2. **Walking by Necessity**: Impoverished, transit-deprived individuals walking along suburban highways, multi-lane arterials, and roads without sidewalks because their car broke down or transit does not exist. This is compelled travel.

---

## Conflating Exercise With Roadside Danger

Framing transportation walking as an unalloyed public health victory overlooks the physical hazards of compelled walking.

According to data compiled by Smart Growth America in their *Dangerous by Design* report, American pedestrian fatalities have climbed to 40-year highs, with low-income and minority pedestrians bearing a disproportionate share of the carnage. Black pedestrians are struck and killed by motor vehicles at rates 82% higher than White pedestrians.

When the CDC data shows that 42.6% of transportation-insecure Black adults walk for daily transportation, that figure cannot be viewed solely as cardiovascular exercise. In the absence of sidewalks, signalized crosswalks, and reduced vehicular speeds, forced pedestrian travel on arterial roads is an environmental exposure associated with severe morbidity and mortality.

---

## Practical Takeaways for Clinicians, Health Systems, and Planners

1. **Avoid Over-Simplistic Prescriptions**: Clinicians advising low-income patients to get more exercise by walking for daily errands must recognize environmental context. If a patient lives in a transit desert with high-speed road corridors, prescribing transportation walking without assessing neighborhood walkability exposes them to vehicular trauma.
2. **Screening for Insecurity Requires Nuance**: The single-item survey question in the NHIS identified only 5.6% of adults with transportation barriers. Validated 16-item clinical instruments, such as the Transportation Security Index, routinely identify four times as many individuals (up to 24%). Health systems screening for social determinants of health should not assume a single binary question captures the logistical complexity of vehicle unreliability.
3. **Planners Must Balance Universal and Targeted Design**: Urban planners cannot rely solely on poverty or transit-insecurity maps to place pedestrian infrastructure. Because 89% of all transportation walkers are transportation secure, universal infrastructure (complete sidewalk networks, safe intersections) is required to sustain population-level physical activity. Simultaneously, targeted interventions in disinvested corridors must focus on physical separation and pedestrian safety, treating compelled walking as an acute injury prevention priority.

The raw CDC data is mathematically sound, but its public health meaning is clear: walking in America remains deeply divided along socioeconomic lines, and treating survival-driven walking as voluntary wellness obscures the systemic infrastructure failures that force people onto the shoulder of the road.

---

## Acknowledgments

Sincere gratitude is extended to Soto et al. for their transparent reporting, rigorous analytical documentation, and dedicated public health surveillance. Their clear delineation of survey variables, exclusion criteria, and complex weighting methods made this independent computational reproduction possible and established an exemplary standard of open scientific reporting.

