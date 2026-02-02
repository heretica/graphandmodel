---
parent: '[[Causal inference]]'
created_by:
- '[[Donald Campbell]]'
part_of: '[[Policy Evaluation]]'
uses: '[[Structural Causal Model]]'
type: technique
tags:
- method
- quasi-experimental
field: '[[Economics]]'
indirectly_uses:
- '[[Graphical models]]'
inferred_by: reasoner
requires_understanding: '[[Graphical models]]'
---
# Regression Discontinuity

## Overview

Regression Discontinuity Design (RDD) is a quasi-experimental evaluation method that estimates causal effects by exploiting discontinuities in treatment assignment rules. When treatment is assigned based on whether a continuous "running variable" crosses a threshold, units just above and below the cutoff are comparable except for treatment status.

## Core Concept

RDD leverages the idea that units just barely above and just barely below a treatment threshold are essentially randomly assigned to treatment, despite the deterministic assignment rule. This creates a **local randomized experiment** at the threshold.

### The Sharp RDD Estimator

In a sharp RDD, treatment assignment changes deterministically at the cutoff c:

$$D_i = \mathbb{1}[X_i \geq c]$$

Where:
- $D_i$ = Treatment indicator (1 if treated, 0 if control)
- $X_i$ = Running variable (e.g., test score, age, poverty index)
- $c$ = Treatment cutoff threshold

The causal effect at the threshold is:

$$\tau = \lim_{x \downarrow c} E[Y_i|X_i=x] - \lim_{x \uparrow c} E[Y_i|X_i=x]$$

This estimates the **local average treatment effect (LATE)** at the discontinuity.

## Historical Foundation

### Thistlethwaite and Campbell (1960)

Donald Campbell and Donald Thistlethwaite introduced regression discontinuity in their 1960 study of merit awards on academic outcomes:

**Research Design:**
- Students with test scores above a cutoff received scholarships
- Students just below the cutoff served as controls
- Compared outcomes for students near the threshold

**Key Insight:** Units near the cutoff are comparable on both observed and unobserved characteristics, making the threshold a "natural experiment."

**Impact:**
- Established RDD as a credible quasi-experimental method
- Showed how deterministic assignment rules can identify causal effects
- Laid groundwork for modern program evaluation

### Hahn, Todd, and Van der Klaauw (2001)

Formalized the statistical foundations and identification assumptions for RDD, establishing it as a rigorous causal inference framework.

## Types of Regression Discontinuity

### Sharp RDD
- Treatment assignment changes deterministically at the cutoff
- Everyone above threshold gets treatment, everyone below doesn't
- Simplest and most transparent design

### Fuzzy RDD
- Treatment probability changes discontinuously at threshold
- Not everyone above cutoff receives treatment
- Requires instrumental variables approach
- Threshold serves as instrument for treatment

### Kink RDD
- Treatment intensity (not assignment) changes at threshold
- Effect estimated from change in slope, not level
- Useful for dose-response relationships

## Key Assumptions

### 1. Continuity of Potential Outcomes

**Assumption:** In the absence of treatment, the relationship between the running variable and outcome would be continuous at the cutoff.

**Implication:** Any discontinuity in observed outcomes at the threshold must be due to treatment.

**Testing:**
- Visual inspection of outcome plot
- Density test for running variable manipulation
- Placebo cutoff tests

### 2. No Manipulation of Running Variable

**Assumption:** Units cannot precisely manipulate their running variable value to change treatment status.

**Violation Example:** Students retaking a test to cross a scholarship threshold.

**Testing:**
- McCrary (2008) density test: Check for discontinuity in running variable density
- Examine baseline covariate balance at threshold

### 3. Local Randomization (Alternative Framework)

Recent work reframes RDD as local randomization within a narrow window around the cutoff, where treatment is "as-if random."

## Advantages

1. **Transparency:** Clear graphical representation of treatment effect
2. **Credibility:** Few assumptions needed compared to other observational methods
3. **Robustness:** Results not sensitive to functional form far from cutoff
4. **Applicability:** Many real-world policies use threshold-based assignment

## Limitations

### 1. External Validity
- Effect only identified at the threshold (LATE)
- May not generalize to populations far from cutoff
- Limited for heterogeneous treatment effects

### 2. Statistical Power
- Only uses observations near threshold
- Requires large samples for precise estimation
- Trade-off between bias (wide bandwidth) and variance (narrow bandwidth)

### 3. Functional Form Dependence
- Results can be sensitive to polynomial order
- Modern practice: use local linear regression with optimal bandwidth
- Robust inference methods recommended

## Implementation

### Bandwidth Selection

Critical choice: How far from threshold to include observations?

**Methods:**
- **MSE-optimal bandwidth:** Minimizes mean squared error (Imbens-Kalyanaraman)
- **Cross-validation:** Out-of-sample prediction error
- **Robust bias-corrected inference:** CCT (Calonico, Cattaneo, Titiunik) approach

### Specification

```python
def rdd_estimate(data, running_var, outcome, cutoff, bandwidth):
    """
    Estimate RDD treatment effect using local linear regression.
    """
    # Subset to bandwidth around cutoff
    near_cutoff = abs(data[running_var] - cutoff) <= bandwidth
    subset = data[near_cutoff]

    # Create treatment indicator
    subset['treated'] = (subset[running_var] >= cutoff).astype(int)

    # Center running variable
    subset['x_centered'] = subset[running_var] - cutoff

    # Local linear regression: Y ~ D + X_centered + D*X_centered
    # Allows different slopes on each side of cutoff
    model = OLS(
        subset[outcome],
        subset[['treated', 'x_centered', 'treated_x_x_centered']]
    )

    # Treatment effect is coefficient on 'treated'
    return model.fit().params['treated']
```

### Visualization

```python
import matplotlib.pyplot as plt

def plot_rdd(data, running_var, outcome, cutoff):
    """Visualize RDD with binned scatter plot."""
    # Create bins
    bins = pd.cut(data[running_var], bins=50)
    binned = data.groupby(bins)[outcome].mean()

    # Separate by treatment
    below = binned[binned.index.mid < cutoff]
    above = binned[binned.index.mid >= cutoff]

    # Plot
    plt.scatter(below.index.mid, below.values, color='blue', label='Control')
    plt.scatter(above.index.mid, above.values, color='red', label='Treated')
    plt.axvline(cutoff, linestyle='--', color='black', label='Threshold')
    plt.xlabel('Running Variable')
    plt.ylabel('Outcome')
    plt.legend()
    plt.title('Regression Discontinuity Plot')
```

## Applications

### Education
- **Class Size Effects:** Maimonides' Rule (Angrist & Lavy, 1999)
  - Schools add classes when enrollment exceeds multiples of 40
  - Discontinuous drops in class size at thresholds

- **Financial Aid:** Merit scholarship cutoffs based on test scores

### Labor Economics
- **Unemployment Insurance:** Benefit eligibility based on prior earnings
- **Minimum Wage:** Age-based wage thresholds

### Health Economics
- **Medicare Eligibility:** Age 65 threshold in the United States
- **Medical Treatment:** Clinical guidelines with cutoff values (e.g., BMI, blood pressure)

### Political Economy
- **Electoral Competition:** Incumbency advantage at 50% vote share
- **Campaign Finance:** Contribution limits based on election outcomes

## Relationship to Other Methods

- **Builds on:** Potential outcomes framework, local randomization
- **Complements:** Difference-in-differences (different identification strategy)
- **Fuzzy RDD uses:** Instrumental variables (threshold as instrument)
- **Requires:** Structural causal models for assumption clarification

## Modern Developments

### Robust Inference
- Bias-corrected confidence intervals (Calonico et al., 2014)
- Robust standard errors accounting for clustering
- Permutation-based inference for small samples

### Machine Learning
- Data-driven bandwidth selection
- Flexible functional forms (random forests, kernels)
- Treatment effect heterogeneity estimation

### Spatial RDD
- Geographic boundaries as discontinuities
- Spatial spillovers and interference
- GIS-based implementation

## Validation and Sensitivity

### Robustness Checks

1. **Alternative Bandwidths:** Show results stable across choices
2. **Alternative Polynomials:** Linear, quadratic, cubic specifications
3. **Placebo Cutoffs:** No discontinuity at false thresholds
4. **Covariate Balance:** Baseline characteristics smooth at cutoff
5. **Donut Hole:** Exclude observations very close to cutoff

### Falsification Tests

- **Density Test:** Running variable smooth at cutoff (McCrary test)
- **Predetermined Outcomes:** No effect on outcomes determined before treatment
- **Bandwidth Sensitivity:** Effect persists across bandwidth choices

## Further Reading

- **Imbens, G. W., & Lemieux, T. (2008).** Regression discontinuity designs: A guide to practice. *Journal of Econometrics*, 142(2), 615-635.
- **Lee, D. S., & Lemieux, T. (2010).** Regression Discontinuity Designs in Economics. *Journal of Economic Literature*, 48(2), 281-355.
- **Cattaneo, M. D., Idrobo, N., & Titiunik, R. (2019).** *A Practical Introduction to Regression Discontinuity Designs: Foundations.* Cambridge University Press.
