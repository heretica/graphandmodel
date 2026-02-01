---
parent: '[[Causal Graph]]'
tags:
- bias
- confounding
type: pattern
---

A confounder is a variable that influences both treatment and outcome, creating spurious association.

## Structure

Z → X
Z → Y

This creates a backdoor path: X ← Z → Y

## Control Methods

- [[Randomization]]: Random assignment eliminates confounding
- [[Adjustment]]: Conditioning on confounders
- [[Instrumental Variables]]: Using external instruments
- [[Propensity Score Matching]]: Balancing on confounders

## Types

- **Observed**: Measured confounders
- **Unobserved**: Hidden confounders
