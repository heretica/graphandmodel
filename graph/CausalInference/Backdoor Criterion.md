---
parent: '[[Causal Graph]]'
tags:
- criterion
- confounding
type: method
used_for: '[[Causal Inference]]'
---

The backdoor criterion identifies sufficient sets of variables to control for confounding.

## Definition

A set Z satisfies the backdoor criterion relative to (X, Y) if:
1. Z blocks all backdoor paths from X to Y
2. Z contains no descendants of X

## Backdoor Path

A path from X to Y with an arrow into X: X ← ... → Y

## Applications

- Identifying valid adjustment sets
- Controlling for confounding
- Enabling causal effect estimation
