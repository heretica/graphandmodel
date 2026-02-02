---
parent: "[[Causality]]"
tags:
  - methodology
type: field
wikidata: Q1195958
related:
  - "[[Statistics]]"
  - "[[Machine Learning]]"
domain_encompasses:
  - "[[Causal inference]]"
  - "[[Policy Evaluation]]"
  - "[[Propensity Score Matching]]"
inferred_by: reasoner
---
Causal inference (Wikidata: Q1195958) is the process of determining cause-and-effect relationships from data. Unlike predictive modeling, which focuses on association, causal inference aims to answer questions about what would happen under interventions or counterfactual scenarios.

The fundamental problem of causal inference, identified by Paul Holland and Donald Rubin, is that we can never observe both potential outcomes for the same unit: we see either the treated or control outcome, but not both. This missing data problem distinguishes causal inference from standard statistical estimation.

```python
# The fundamental problem
def causal_effect(unit):
    # We want to compute: Y(1) - Y(0)
    # But we only observe one potential outcome
    if unit.treated:
        observed = unit.Y_1  # We see this
        missing = unit.Y_0   # We never see this
    else:
        observed = unit.Y_0  # We see this
        missing = unit.Y_1   # We never see this
    return missing - observed  # Impossible!
```

Three core challenges complicate causal inference. Confounding occurs when variables affect both treatment and outcome, creating spurious associations. Selection bias arises when the sample is not representative of the population. Reverse causation happens when the effect influences the cause, making causal direction ambiguous.

Gold standard methods include [[Randomized Controlled Trial]], [[Instrumental Variables]], [[Propensity Score Matching]], [[Difference-in-Differences]], and [[Regression Discontinuity]]. Each method makes different assumptions and suits different research designs.
