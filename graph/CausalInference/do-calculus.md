---
parent: '[[Structural Causal Model]]'
tags:
- method
- intervention
type: calculus
created_by: '[[Judea Pearl]]'
---

The do-calculus is a set of inference rules for causal reasoning developed by Judea Pearl.

## do-operator

- **Observation**: P(Y|X=x) - seeing X=x
- **Intervention**: P(Y|do(X=x)) - setting X=x externally

## Three Rules

1. **Insertion/deletion of observations**
2. **Action/observation exchange**
3. **Insertion/deletion of actions**

## Applications

- Computing causal effects from observational data
- Determining identifiability of causal queries
- Deriving adjustment formulas
