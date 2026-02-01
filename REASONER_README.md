# Obsidian Graph Reasoner

A demonstration of logical reasoning on top of an Obsidian vault using [Semantica Hawksight](https://www.semantica.ai/)'s reasoning engine.

## Overview

This project shows how to extract relationships from Obsidian markdown files and apply logical inference rules to discover new knowledge automatically.

## Files

- `obsidian_graph_reasoner.py` - Full-featured reasoner that reads your Obsidian vault
- `example_simple_reasoner.py` - Simple standalone example with hardcoded facts
- `requirements.txt` - Python dependencies

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have the Semantica Hawksight library installed:
```bash
pip install semantica-hawksight
```

## Quick Start

### Option 1: Simple Example (No Obsidian vault needed)

Run the simple example to see the reasoner in action:

```bash
python example_simple_reasoner.py
```

This will demonstrate inference on a small set of hardcoded facts about ML models.

### Option 2: Full Obsidian Vault Reasoner

Run the full reasoner on your Obsidian vault:

```bash
python obsidian_graph_reasoner.py
```

This will:
1. Scan all markdown files in the `graph/` directory
2. Extract relationships from YAML frontmatter
3. Apply reasoning rules
4. Display inferred knowledge

## How It Works

### 1. Extracting Facts from Obsidian

The reasoner reads YAML frontmatter from your markdown files:

```yaml
---
parent: "[[Model]]"
type_model:
  - "[[Classification]]"
usage: "[[Prediction]]"
---
```

And converts it to logical facts:
- `Model PARENT_OF Classification`
- `LogisticRegression IS_A Classification`
- `LinearRegression USED_FOR Prediction`

### 2. Defining Reasoning Rules

Rules define how to infer new knowledge:

```python
from semantica.reasoning import Reasoner, Rule

reasoner = Reasoner()

# Example: Ancestor rule
reasoner.add_rule(Rule(
    name="ancestor_rule",
    conditions=["?a PARENT_OF ?b", "?b PARENT_OF ?c"],
    conclusions=["?a ANCESTOR_OF ?c"]
))

# Example: Usage inheritance
reasoner.add_rule(Rule(
    name="usage_inheritance",
    conditions=["?a IS_A ?b", "?b USED_FOR ?c"],
    conclusions=["?a CAN_BE_USED_FOR ?c"]
))
```

### 3. Inferring New Facts

The reasoner applies rules to discover new relationships:

```python
facts = [
    "Model PARENT_OF Classification",
    "Classification PARENT_OF LogisticRegression",
    "Classification USED_FOR Prediction"
]

new_facts = reasoner.infer_facts(facts)
# Result: ['Model ANCESTOR_OF LogisticRegression',
#          'LogisticRegression CAN_BE_USED_FOR Prediction']
```

## Supported Relationships

The reasoner extracts these relationship types from Obsidian frontmatter:

| Frontmatter Key | Relation | Example |
|----------------|----------|---------|
| `parent` | `PARENT_OF` | Model PARENT_OF Classification |
| `type_model` | `IS_A` | LogisticRegression IS_A Classification |
| `type_algo` | `IS_ALGORITHM_FOR` | GradientDescent IS_ALGORITHM_FOR Optimization |
| `usage` | `USED_FOR` | Regression USED_FOR Prediction |

## Built-in Reasoning Rules

The reasoner includes these inference rules:

1. **Ancestor Rule**: Discovers transitive hierarchies
   - If A → B and B → C, then A is ancestor of C

2. **Type Inheritance**: Propagates type information up hierarchies
   - If A is-a B and C is parent of B, then A belongs to C

3. **Usage Inheritance**: Propagates usage from types to instances
   - If A is-a B and B is used for C, then A can be used for C

4. **Shared Type**: Finds similar entities
   - If A is-a X and B is-a X, then A is similar to B

5. **Algorithm Applicability**: Domain inference for algorithms
   - If A is algorithm for B and C is parent of B, then A is applicable to C

## Example Output

```
================================================================================
OBSIDIAN GRAPH REASONER - SUMMARY
================================================================================

Vault path: /home/user/graphandmodel/graph
Original facts extracted: 15
New facts inferred: 8

================================================================================
ORIGINAL FACTS:
================================================================================
  • Classification IS_A Model
  • Clustering IS_A Model
  • LinearRegression IS_A Regression
  • LinearRegression USED_FOR Prediction
  • LogisticRegression IS_A Classification
  • Model PARENT_OF Classification
  • Model PARENT_OF Clustering
  • Model PARENT_OF Regression
  • Regression IS_A Model
  • Regression USED_FOR Prediction

================================================================================
INFERRED FACTS:
================================================================================
  ✓ LinearRegression BELONGS_TO Model
  ✓ LinearRegression CAN_BE_USED_FOR Prediction
  ✓ LogisticRegression BELONGS_TO Model
  ✓ LogisticRegression SIMILAR_TO LinearRegression
  ✓ Model ANCESTOR_OF LinearRegression
  ✓ Model ANCESTOR_OF LogisticRegression
```

## Customization

### Adding New Relationship Types

Edit `obsidian_graph_reasoner.py` to extract additional frontmatter fields:

```python
# In extract_facts_from_file method
elif key == 'your_custom_field':
    if isinstance(value, list):
        for item in value:
            item_name = self.parse_wikilink(item)
            facts.append(f"{subject} YOUR_RELATION {item_name}")
```

### Adding New Reasoning Rules

Add custom rules in the `add_reasoning_rules` method:

```python
# In add_reasoning_rules method
self.reasoner.add_rule(Rule(
    name="your_rule_name",
    conditions=["?a RELATION1 ?b", "?b RELATION2 ?c"],
    conclusions=["?a NEW_RELATION ?c"]
))
```

## Use Cases

1. **Knowledge Discovery**: Automatically find implicit relationships in your notes
2. **Consistency Checking**: Validate that your knowledge graph is logically consistent
3. **Query Enhancement**: Use inferred facts to improve search and queries
4. **Ontology Building**: Build formal ontologies from informal note structures
5. **Documentation**: Generate relationship diagrams showing both explicit and inferred links

## Integration with Existing Tools

This reasoner complements the existing RAG engines in the `rag/` directory:
- Use the reasoner to discover relationships
- Feed inferred facts into the KnowledgeGraphIndex
- Enhance PropertyGraphIndex with logical inference
- Improve vector search relevance with relationship context

## Further Reading

- [Semantica Hawksight Documentation](https://www.semantica.ai/docs)
- [Obsidian Documentation](https://help.obsidian.md/)
- [Knowledge Graphs and Reasoning](https://en.wikipedia.org/wiki/Knowledge_graph)

## License

See LICENSE file in the root directory.
