---
parent: '[[Causal Graph]]'
tags:
- graph-theory
- independence
type: criterion
wikidata: Q5203133
---

d-separation (directed separation, Wikidata: Q5203133) is a graphical criterion that determines when two sets of variables are conditionally independent given a third set. Developed by Judea Pearl, it provides the link between causal graphs and probability distributions.

> "d-separation is complete: if X and Y are d-separated by Z in the graph, they are conditionally independent given Z in every distribution compatible with that graph." — Judea Pearl

A path between X and Y is blocked by conditioning set Z according to three rules. First, if the path contains a chain X → M → Y or fork X ← M → Y, and M is in Z, the path is blocked. Second, if the path contains a collider X → M ← Y, and neither M nor its descendants are in Z, the path is blocked.

```python
def is_d_separated(graph, X, Y, Z):
    """Check if X and Y are d-separated given Z."""
    for path in graph.all_paths(X, Y):
        if not is_blocked(path, Z):
            return False
    return True

def is_blocked(path, Z):
    """Check if a path is blocked by conditioning set Z."""
    for node in path:
        if is_chain_or_fork(node, path) and node in Z:
            return True
        if is_collider(node, path) and node not in Z:
            return True
    return False
```

The power of d-separation lies in its graphical nature: we can read conditional independencies directly from the causal graph without examining data. This enables the [[Backdoor Criterion]] for identifying valid adjustment sets and the [[do-calculus]] for computing causal effects from observational data.
