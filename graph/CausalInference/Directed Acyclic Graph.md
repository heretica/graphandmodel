---
parent: '[[Graph Theory]]'
tags:
- graph
- data-structure
type: structure
used_in: '[[Structural Causal Model]]'
---

A Directed Acyclic Graph (DAG) is a graph with directed edges and no cycles.

## Properties

- **Directed**: Edges have a direction (A → B)
- **Acyclic**: No path from a node back to itself
- **Topological Ordering**: Nodes can be linearly ordered

## In Causal Models

DAGs represent causal relationships where:
- Nodes = Variables
- Edges = Direct causal effects
- Paths = Causal pathways

## Key Concepts

- [[d-separation]]: Graphical criterion for conditional independence
- [[Collider]]: Node with multiple incoming edges
- [[Confounder]]: Common cause of two variables
