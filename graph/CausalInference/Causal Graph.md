---
parent: '[[Directed Acyclic Graph]]'
tags:
- causal-inference
- graph
type: representation
part_of: '[[Structural Causal Model]]'
---

A causal graph is a DAG where edges represent direct causal relationships.

## Components

- **Nodes**: Variables in the system
- **Directed Edges**: X → Y means X causes Y
- **Paths**: Sequences of edges showing causal flow

## Types of Paths

- **Chain**: X → M → Y (mediation)
- **Fork**: X ← Z → Y (confounding)
- **Collider**: X → Z ← Y (selection bias)

## Applications

- Identifying confounders
- Determining adjustment sets
- Planning interventions
