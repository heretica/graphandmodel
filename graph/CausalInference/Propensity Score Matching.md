---
parent: '[[Causal Inference]]'
tags:
- method
- matching
type: technique
---

Propensity score matching balances treatment and control groups on observed covariates.

## Propensity Score

Probability of treatment given covariates: e(X) = P(T=1|X)

## Methods

- **Nearest neighbor matching**
- **Caliper matching**
- **Stratification**
- **Inverse probability weighting**

## Assumptions

- Unconfoundedness (no unmeasured confounding)
- Common support (overlap)
- Correct propensity score specification
