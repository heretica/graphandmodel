---
parent: [[Causal Inference]]
created_by: [[Donald Rubin]]
part_of: [[Propensity Score Matching]]
uses: [[Structural Causal Model]]
used_for: [[Policy Evaluation]]
---

# Inverse Probability Weighting

Inverse Probability Weighting (IPW) is a statistical technique used to adjust for confounding in observational studies. It creates a pseudo-population in which treatment assignment is independent of measured confounders.

## How It Works

The method assigns weights to observations based on the inverse of their propensity scores, making the weighted sample representative of the population that would have been obtained in a randomized experiment.

## Applications

- Causal effect estimation
- Missing data handling
- Survey sampling adjustments
- Treatment effect heterogeneity

## Related Methods

This technique is closely related to [[Propensity Score Matching]] and is often used in combination with other causal inference methods for robust effect estimation.
