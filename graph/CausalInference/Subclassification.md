---
parent: '[[Causal Inference]]'
uses: '[[Rubin Causal Model]]'
type: technique
tags:
- method
- matching
related_to: '[[Propensity Score Matching]]'
---
Subclassification (also called stratification) is a causal inference method that estimates treatment effects by dividing units into homogeneous subgroups based on observed covariates. Within each subclass, treated and control units are assumed comparable, allowing unbiased estimation of causal effects.

## Conceptual Foundation

Subclassification operationalizes the **Rubin Causal Model** by:

1. Defining subclasses where treated and control units have similar covariate distributions
2. Estimating treatment effects within each subclass
3. Aggregating across subclasses using weighted averages

The method assumes **unconfoundedness within subclasses**: conditioning on covariates blocks all backdoor paths between treatment and outcome.

## Mathematical Framework

### Subclass Formation

  
Divide the covariate space into $K$ mutually exclusive subclasses $S_1, S_2, \ldots, S_K$ such that:

- Units within each subclass are homogeneous on covariates
- Treatment assignment is unconfounded within each subclass

### Within-Subclass Estimation

  
For subclass $k$, estimate the average treatment effect:

  

$$\hat{\tau}_k = \bar{Y}_{1k} - \bar{Y}_{0k}$$

  

Where:

- $\bar{Y}_{1k}$ = Average outcome for treated units in subclass $k$

- $\bar{Y}_{0k}$ = Average outcome for control units in subclass $k$

  

### Overall Effect

  

Aggregate using weights proportional to subclass size:

  

$$\hat{\tau} = \sum_{k=1}^{K} w_k \hat{\tau}_k$$

  

Where $w_k = n_k / n$ and $n_k$ is the number of units in subclass $k$.

  

## Cochran's Rule

  

**William Cochran (1968)** showed that:

- **5 subclasses** remove approximately **90% of bias** due to a single continuous confounder

- Further refinement yields diminishing returns

- Practical guideline: 5-10 subclasses for most applications

  

This result established subclassification as an efficient method for bias reduction with minimal modeling assumptions.

  

## Implementation Methods

  

### 1. Quantile-Based Subclassification

  

Divide covariates into quantiles (quintiles, deciles):

  

```python

def quantile_subclassification(data, covariate, n_subclasses=5):

"""

Create subclasses based on covariate quantiles.

"""

data['subclass'] = pd.qcut(

data[covariate],

q=n_subclasses,

labels=False

)

return data

```

  

### 2. Propensity Score Subclassification

  

Use propensity scores to define subclasses:

  

```python

def propensity_subclassification(data, treatment, covariates, n_subclasses=5):

"""

Subclassify on propensity score.

"""

# Estimate propensity scores

ps_model = LogisticRegression()

ps_model.fit(covariates, treatment)

ps = ps_model.predict_proba(covariates)[:, 1]

  

# Create subclasses

data['subclass'] = pd.qcut(ps, q=n_subclasses, labels=False)

return data

  

def estimate_ate(data, outcome, treatment, subclass_col='subclass'):

"""

Estimate ATE by averaging within-subclass effects.

"""

effects = []

weights = []

  

for subclass in data[subclass_col].unique():

subset = data[data[subclass_col] == subclass]

  

# Within-subclass treatment effect

y1 = subset[subset[treatment] == 1][outcome].mean()

y0 = subset[subset[treatment] == 0][outcome].mean()

effect = y1 - y0

  

effects.append(effect)

weights.append(len(subset) / len(data))

  

# Weighted average

ate = np.average(effects, weights=weights)

return ate

```

  

### 3. Multivariate Subclassification

  

For multiple confounders, use:

- **Mahalanobis distance** to create subclasses

- **Decision trees** to partition covariate space

- **Clustering algorithms** (k-means, hierarchical)

  

## Advantages

  

1. **Transparency**: Easy to visualize and understand

2. **Robustness**: Less sensitive to functional form misspecification

3. **Diagnostics**: Can check covariate balance within each subclass

4. **Flexibility**: Works with continuous or categorical confounders

  

## Limitations

  

### 1. Curse of Dimensionality

  

With many covariates, creating balanced subclasses becomes difficult:

- Number of possible subclasses grows exponentially

- Sparse data in high-dimensional subclass combinations

- **Solution**: Use propensity score dimension reduction

  

### 2. Residual Confounding

  

If subclasses are too coarse, residual imbalance remains:

- Within-subclass heterogeneity on confounders

- Bias not fully eliminated

- **Solution**: Use finer subclassification or regression adjustment within subclasses

  

### 3. Efficiency Loss

  

Compared to regression:

- Discards information by discretizing continuous variables

- Can have larger standard errors

- **Trade-off**: Robustness vs. efficiency

  

## Cochran's Original Study

  

**Context**: Evaluating the effect of smoking on lung function

  

**Design:**

- Stratified on age (continuous confounder)

- Compared smokers and non-smokers within age strata

- Showed that 5 age strata removed most confounding

  

**Finding**: The "magic number" of 5 subclasses became a widely-used heuristic in epidemiology and observational studies.

  

## Relationship to Other Methods

  

### Compared to Regression

  

| Aspect | Subclassification | Regression |

|--------|-------------------|------------|

| Assumptions | Unconfounded within subclass | Correct functional form |

| Flexibility | Non-parametric within subclass | Parametric |

| Efficiency | Lower (discretization) | Higher (uses full data) |

| Robustness | More robust to misspecification | Sensitive to model choice |

  

### Compared to Matching

  

| Aspect | Subclassification | Matching |

|--------|-------------------|----------|

| Unit utilization | Uses all units | May discard unmatched units |

| Computation | Simple, fast | Can be complex |

| Exact balance | Approximate | Can achieve exact balance |

  

### Combined Approaches

  

**Subclassification + Regression:**

- Create subclasses on covariates

- Run regression within each subclass

- Aggregate effects

- **Benefit**: Reduces model dependence while maintaining efficiency

  

## Applications

  

### Public Health

- Smoking and health outcomes (Cochran's original application)

- Vaccine effectiveness studies

- Environmental exposure effects

  

### Economics

- Labor market interventions

- Education program evaluation

- Minimum wage effects

  

### Clinical Research

- Observational studies of treatment effects

- Post-market drug surveillance

- Comparative effectiveness research

  

## Modern Developments

  

### Double Robustness

  

Combine subclassification with outcome modeling:

- Subclassify on propensity score

- Model outcomes within subclasses

- Estimator is consistent if either model is correct

  

### Machine Learning Integration

  

Use ML for:

- Automatic subclass formation (decision trees, random forests)

- Optimal number of subclasses (cross-validation)

- Adaptive subclassification rules

  

### High-Dimensional Extensions

  

- **Lasso** for covariate selection before subclassification

- **Bayesian nonparametric** methods for infinite subclasses

- **Kernel methods** for continuous subclassification

  

## Validation and Diagnostics

  

### Balance Checks

  

Within each subclass, verify:

  

```python

def check_balance(data, covariates, treatment, subclass_col='subclass'):

"""

Check covariate balance within subclasses.

"""

for subclass in data[subclass_col].unique():

subset = data[data[subclass_col] == subclass]

  

for cov in covariates:

treated_mean = subset[subset[treatment] == 1][cov].mean()

control_mean = subset[subset[treatment] == 0][cov].mean()

std_diff = abs(treated_mean - control_mean) / subset[cov].std()

  

print(f"Subclass {subclass}, {cov}: SMD = {std_diff:.3f}")

```

  

**Guideline**: Standardized mean difference < 0.1 indicates good balance

  

### Overlap Assessment

  

Ensure common support within each subclass:

- Check treatment and control units exist in each subclass

- Flag subclasses with extreme imbalance (e.g., >90% treated)

  

### Sensitivity Analysis

  

Test robustness to:

- Number of subclasses (vary $K$ from 3 to 20)

- Covariate choice for subclass formation

- Weighting scheme (equal weights vs. proportional)

  

## Further Reading

  

- **Cochran, W. G. (1968).** The effectiveness of adjustment by subclassification in removing bias in observational studies. *Biometrics*, 24(2), 295-313.

- **Rosenbaum, P. R., & Rubin, D. B. (1984).** Reducing bias in observational studies using subclassification on the propensity score. *Journal of the American Statistical Association*, 79(387), 516-524.

- **Imbens, G. W., & Rubin, D. B. (2015).** *Causal Inference for Statistics, Social, and Biomedical Sciences: An Introduction.* Cambridge University Press.