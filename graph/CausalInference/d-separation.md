---
parent: '[[Causal Graph]]'
tags:
- graph-theory
- independence
type: criterion
---

d-separation (directed separation) is a graphical criterion for conditional independence in DAGs.

## Definition

Two sets of nodes X and Y are d-separated by Z if all paths between X and Y are blocked by Z.

## Blocking Rules

A path is blocked if it contains:
1. **Chain** X → M → Y with M in Z
2. **Fork** X ← M → Y with M in Z
3. **Collider** X → M ← Y with M and descendants NOT in Z

## Applications

- Identifying conditional independencies
- Determining minimal adjustment sets
- Testing causal assumptions
