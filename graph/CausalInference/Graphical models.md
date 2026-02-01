---
parent: '[[Statistics]]'
type: concept
tags:
- framework
- graph-theory
---
Graphical models use graph-structured representations to encode probability distributions and conditional independence relationships between variables. They provide a unified framework for probabilistic reasoning and causal inference.

## Types

* ***Directed Graphical Models**: Bayesian networks, causal graphs
* **Undirected Graphical Models**: Markov random fields
* **Chain Graphs**: Mix of directed and undirected edges

## Applications

Graphical models form the mathematical foundation for structural causal models, Bayesian inference, and many machine learning algorithms.

## Key Properties

- **Factorization**: Joint probability factors according to graph structure
- **d-separation**: Graph-based conditional independence
- **Markov Property**: Variables are independent of non-descendants given parents

  

## Historical Development

Graphical models emerged from the intersection of probability theory, graph theory, and statistics. Judea Pearl's work on Bayesian networks in the 1980s popularized the framework, showing how graphs could represent causal relationships and enable efficient probabilistic inference.
## Relationship to Causal Inference

Graphical models provide the formal mathematical foundation for causal inference. Directed acyclic graphs (DAGs) represent causal structures, where edges indicate direct causal effects and the graph topology encodes conditional independence assumptions.

  

## Further Reading

  

- Pearl, J. (1988). *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann.

- Koller, D., & Friedman, N. (2009). *Probabilistic Graphical Models: Principles and Techniques*. MIT Press.