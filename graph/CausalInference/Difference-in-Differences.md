---
parent: '[[Causal inference]]'
created_by:
- '[[David Card]]'
part_of: '[[Policy Evaluation]]'
uses:
- '[[Structural Causal Model]]'
- '[[Rubin Causal Model]]'
used_for:
- '[[Policy Evaluation]]'
field: '[[Economics]]'
indirectly_uses:
- '[[Graphical models]]'
- '[[Structural Causal Model]]'
inferred_by: reasoner
requires_understanding:
- '[[Structural Causal Model]]'
- '[[Graphical models]]'
---
## Overview

Difference-in-Differences (DiD) is a quasi-experimental research design used to estimate causal effects by comparing the changes in outcomes over time between a treatment group and a control group. This method is particularly valuable when randomized controlled trials are infeasible or unethical.

## Core Concept

The DiD approach exploits variation in treatment timing across groups to identify causal effects. It compares the difference in outcomes before and after treatment for the treated group (first difference) with the difference for the control group (second difference), hence "difference-in-differences."

### The DiD Estimator

The basic DiD estimator can be expressed as:

$$\hat{\delta}_{DiD} = (\bar{Y}_{treat,post} - \bar{Y}_{treat,pre}) - (\bar{Y}_{control,post} - \bar{Y}_{control,pre})$$

Where:
- $\bar{Y}_{treat,post}$ = Average outcome for treated group after treatment
- $\bar{Y}_{treat,pre}$ = Average outcome for treated group before treatment
- $\bar{Y}_{control,post}$ = Average outcome for control group after treatment period
- $\bar{Y}_{control,pre}$ = Average outcome for control group before treatment period

## The Parallel Trends Assumption

**Critical Identifying Assumption:** In the absence of treatment, the treatment and control groups would have followed parallel trends over time.

This means:
- The control group represents the counterfactual trend for the treatment group
- Any pre-existing differences between groups remain constant over time
- Only the treatment causes divergence from parallel trends

**Testing Parallel Trends:**
- Examine pre-treatment trends graphically
- Conduct formal pre-trend tests
- Use event study specifications with leads and lags
- Consider alternative estimation strategies if assumption fails

## Historical Foundation

### The Card-Krueger Study (1994)

David Card and Alan Krueger's landmark study on minimum wage effects revolutionized labor economics and popularized the DiD method:

**Research Question:** Does raising the minimum wage reduce employment?

**Natural Experiment:**
- **Treatment Group:** Fast-food restaurants in New Jersey (minimum wage increased from \$4.25 to \$5.05)
- **Control Group:** Fast-food restaurants in neighboring Pennsylvania (no change)
- **Outcome:** Employment levels before and after the wage increase

**Findings:**
- No evidence that minimum wage increase reduced employment
- Challenged conventional economic theory
- Demonstrated the power of quasi-experimental methods

**Impact:**
- Shifted empirical focus toward natural experiments
- Established DiD as a credible causal inference tool
- Won Card the Nobel Prize in Economics (2021)

## Advantages

1. **Natural Experiments:** Leverages real-world policy changes and natural variation
2. **Removes Time-Invariant Confounding:** Controls for time-invariant differences between groups
3. **Intuitive Interpretation:** Easy to visualize and communicate to policymakers
4. **Flexible Framework:** Can be extended to multiple time periods, multiple groups, and staggered adoption

## Limitations and Challenges

### 1. Parallel Trends Assumption
- **Challenge:** Untestable for the post-treatment period
- **Solution:** Robust pre-trend testing, sensitivity analyses, alternative control groups

### 2. Anticipation Effects
- **Challenge:** Treatment effects may begin before formal implementation
- **Example:** Employers anticipating minimum wage increase may adjust hiring earlier
- **Solution:** Exclude periods immediately before treatment, test for anticipatory behavior

### 3. Time-Varying Confounders
- **Challenge:** Factors affecting groups differentially over time
- **Solution:** Include time-varying controls, use triple-differences, synthetic control methods

### 4. Treatment Effect Heterogeneity
- **Challenge:** Effects may vary across units and time
- **Solution:** Event study designs, heterogeneity-robust estimators, group-specific trends

## Modern Extensions

### Staggered DiD
When treatment is adopted at different times across units:
- Requires careful attention to treatment effect heterogeneity
- Recent developments: Callaway & Sant'Anna (2021), Sun & Abraham (2021)
- Addresses issues with two-way fixed effects estimators

### Event Study Specification
$$Y_{it} = \alpha_i + \lambda_t + \sum_{k \neq -1} \beta_k D_{it}^k + \epsilon_{it}$$

Where:
- $\alpha_i$ = Unit fixed effects
- $\lambda_t$ = Time fixed effects
- $D_{it}^k$ = Indicators for periods relative to treatment
- $k = -1$ is the omitted reference period

### Synthetic Control Method
- Constructs a weighted combination of control units to match pre-treatment characteristics
- Particularly useful when few control units are available
- Developed by Abadie, Diamond, and Hainmueller

## Applications in Policy Evaluation

### Labor Economics
- Minimum wage effects (Card & Krueger, 1994)
- Job training program evaluation
- Unemployment insurance impacts

### Health Economics
- Health insurance expansions (Oregon Health Insurance Experiment)
- Hospital quality improvements
- Public health interventions

### Environmental Economics
- Carbon pricing policies
- Environmental regulation impacts
- Renewable energy subsidies

### Education
- Class size reduction effects
- School choice programs
- Teacher incentive policies

## Implementation Considerations

### Data Requirements
- Panel data with pre- and post-treatment periods
- Clear treatment and control groups
- Multiple pre-treatment periods (for testing parallel trends)
- Sufficient sample size for statistical power

### Specification Choices
1. **Regression Framework:**
   - Two-way fixed effects (TWFE)
   - Event study specification
   - Heterogeneity-robust estimators

2. **Standard Errors:**
   - Cluster at treatment level
   - Consider serial correlation
   - Robust to heteroskedasticity

3. **Covariates:**
   - Time-varying controls
   - Group-specific trends
   - Flexible time effects

## Relationship to Other Methods

- **Builds on:** Causal inference framework, potential outcomes
- **Complements:** Regression discontinuity, instrumental variables, synthetic control
- **Requires:** Structural causal models to clarify identifying assumptions
- **Supports:** Evidence-based policy evaluation

## Further Reading

- **Angrist, J. D., & Pischke, J. S. (2009).** *Mostly Harmless Econometrics: An Empiricist's Companion.* Princeton University Press.
- **Card, D., & Krueger, A. B. (1994).** Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania. *American Economic Review*, 84(4), 772-793.
- **Roth, J., Sant'Anna, P. H., Bilinski, A., & Poe, J. (2023).** What's trending in difference-in-differences? A synthesis of the recent econometrics literature. *Journal of Econometrics*, 235(2), 2218-2244.
