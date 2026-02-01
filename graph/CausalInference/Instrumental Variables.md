---
parent: '[[Causal Inference]]'
tags:
- method
- econometrics
type: technique
used_for: '[[Confounding Control]]'
---

Instrumental variables (IV) is a method for estimating causal effects in the presence of unobserved confounding.

## Requirements

An instrument Z must:
1. **Relevance**: Z affects treatment X
2. **Exclusion**: Z affects outcome Y only through X
3. **Independence**: Z is independent of confounders

## Estimation

Causal effect = Cov(Y,Z) / Cov(X,Z)

## Examples

- Randomized encouragement designs
- Natural experiments
- Mendelian randomization (genetics as IV)
