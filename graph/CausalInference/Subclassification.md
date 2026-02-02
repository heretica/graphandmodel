---
parent: "[[Causal inference]]"
uses: "[[Rubin Causal Model]]"
type: technique
tags:
  - method
  - matching
related_to: "[[Propensity Score Matching]]"
---
Subclassification (also called stratification) is a causal inference method that estimates treatment effects by dividing units into homogeneous subgroups based on observed covariates. Within each subclass, treated and control units are assumed comparable, allowing unbiased estimation of causal effects.


Subclassification operationalizes the **Rubin Causal Model** by:

1. Defining subclasses where treated and control units have similar covariate distributions
2. Estimating treatment effects within each subclass
3. Aggregating across subclasses using weighted averages

The method assumes **unconfoundedness within subclasses**: conditioning on covariates blocks all backdoor paths between treatment and outcome.
