---
parent: '[[Machine Learning]]'
tags:
- ethics
- ai
- fairness
type: application
uses:
- '[[Structural Causal Model]]'
- '[[Counterfactual]]'
---

Causal inference provides formal frameworks for fairness in ML systems.

## Causal Fairness Criteria

- **Counterfactual Fairness**: Decision unchanged in counterfactual world
- **Path-Specific Fairness**: Blocking unfair causal pathways
- **Interventional Fairness**: Fair under hypothetical interventions

## Advantages over Statistical Fairness

- Distinguishes legitimate from illegitimate influences
- Handles proxy variables properly
- Provides actionable interventions

## Tools

- [[Causal Graph]]: Represents fairness assumptions
- [[Counterfactual]]: Individual-level fairness
- [[Mediation Analysis]]: Identifying discrimination pathways
