# Obsidian Graph Reasoner

A reasoning engine for Obsidian knowledge graphs that automatically infers new relationships and enriches your knowledge base.

## 🏗️ Architecture

The system follows a clean, modular architecture:

```
src/
├── obsidian_reasoner/          # Core reasoning engine
│   ├── extractor.py            # Extract facts from Obsidian vault
│   ├── reasoner.py             # Apply inference rules
│   ├── persister.py            # Write discoveries back to vault
│   └── models.py               # Data models (Fact, etc.)
├── cli/                        # Command-line interface
│   ├── analyze.py              # Analyze and display inferences
│   └── persist.py              # Persist discoveries to vault
└── importers/                  # External data importers
    └── wikidata.py             # Import from Wikidata
```

## ✨ Features

- **Automatic Fact Extraction**: Parses YAML frontmatter from Obsidian markdown files
- **Logical Reasoning**: Applies 12 inference rules (6 domain-specific + 6 OWL-inspired) to discover new relationships:

  **Domain-Specific Rules:**
  1. **Transitive Parent** (ANCESTOR_OF): If A parent of B, and B parent of C → A ancestor of C
  2. **Transitive Part-Of** (TRANSITIVELY_PART_OF): If A part of B, and B part of C → A transitively part of C
  3. **Contribution** (CONTRIBUTED_TO): If Creator created X, and X part of Y → Creator contributed to Y
  4. **Indirect Usage** (INDIRECTLY_USES): If A uses X, and X uses Y → A indirectly uses Y
  5. **Domain Encompasses** (DOMAIN_ENCOMPASSES): If A parent of X, and X part of Y → A's domain encompasses Y
  6. **Theory Application** (THEORY_APPLIED_BY): If Creator created Theory, and Method uses Theory → Creator's theory applied by Method

  **OWL-Inspired Rules:**
  7. **Symmetric Collaboration** (COAUTHOR_OF, COLLABORATES_WITH): If A coauthor of B → B coauthor of A (symmetric property)
  8. **Inverse Properties** (CREATED_BY, USED_BY, HAS_PART): Automatically generate inverse relationships (owl:inverseOf)
  9. **Methodology Inheritance** (INHERITS_METHODOLOGY_FROM): If Method is_a ParentMethod, ParentMethod uses Technique → Method inherits from Technique
  10. **Field Contribution** (CONTRIBUTED_TO_FIELD): If Person created Method, Method works_in Field → Person contributed to Field
  11. **Cross-Domain Bridges** (BRIDGES_DOMAIN): Detects methods that integrate theories from multiple fields
  12. **Prerequisite Chain** (REQUIRES_UNDERSTANDING): Creates transitive learning dependencies

- **Automated Discovery Persistence**: Writes inferred facts back to your Obsidian vault
- **CI/CD Integration**: GitHub Actions automatically runs reasoning when you add new notes

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package (optional)
pip install -e .
```

### Usage

#### Analyze your knowledge graph

```bash
python src/cli/analyze.py
```

This will:
1. Extract all facts from your Obsidian vault (`graph/` directory)
2. Apply reasoning rules to infer new relationships
3. Display statistics and insights about your knowledge graph

#### Persist discoveries back to your vault

```bash
python src/cli/persist.py
```

This will:
1. Run the reasoner
2. Write inferred facts back to your markdown files as YAML frontmatter
3. Add `inferred_by: reasoner` metadata to track automated discoveries

### Example

**Input** - Your Obsidian vault contains:

`Difference-in-Differences.md`:
```yaml
---
parent: '[[Causal Inference]]'
created_by: '[[David Card]]'
part_of: '[[Policy Evaluation]]'
uses: '[[Structural Causal Model]]'
---
```

`Causal Inference.md`:
```yaml
---
parent: '[[Causality]]'
---
```

`Structural Causal Model.md`:
```yaml
---
created_by: '[[Judea Pearl]]'
---
```

**Output** - The reasoner infers and adds to files:

To `Causality.md`:
```yaml
ancestor_of:
  - '[[Difference-in-Differences]]'
inferred_by: reasoner
```

To `David Card.md`:
```yaml
contributed_to:
  - '[[Policy Evaluation]]'
inferred_by: reasoner
```

To `Judea Pearl.md`:
```yaml
theory_applied_by:
  - '[[Difference-in-Differences]]'
inferred_by: reasoner
```

## 🔄 Automated Workflow

The GitHub Actions workflow (`.github/workflows/reasoning-workflow.yml`) automatically:

1. **Triggers** when you push new `.md` files to the `graph/` directory
2. **Analyzes** your knowledge graph
3. **Persists** new discoveries
4. **Commits** the enriched files back to your repository

This means your Obsidian vault on GitHub stays synchronized with inferred knowledge!

## 📊 Supported Relationships

### Input Relations (from YAML frontmatter)

Users can add these relationships manually in markdown file frontmatter:

- `parent`: Creates PARENT_OF relationship
- `type_model`: Creates IS_A relationship
- `part_of`: Creates PART_OF relationship
- `uses`: Creates USES relationship
- `created_by`: Creates CREATED relationship
- `field` / `works_in`: Creates WORKS_IN relationship
- `used_for`: Creates USED_FOR relationship
- `coauthor_of`: Creates COAUTHOR_OF relationship (symmetric)
- `collaborates_with`: Creates COLLABORATES_WITH relationship (symmetric)

### Inferred Relations (Written to YAML frontmatter)

The reasoner infers these relationships and writes them back to markdown files:

#### Domain-Specific Inferred Relations

| Relation | YAML Key | Description | Example |
|----------|----------|-------------|---------|
| `ANCESTOR_OF` | `ancestor_of` | Grandparent in hierarchy | Causality → Difference-in-Differences |
| `TRANSITIVELY_PART_OF` | `transitively_part_of` | Transitive composition | Component → System → Platform |
| `CONTRIBUTED_TO` | `contributed_to` | Creator's contribution to field | David Card → Policy Evaluation |
| `INDIRECTLY_USES` | `indirectly_uses` | Transitive dependency | App → Framework → Language |
| `DOMAIN_ENCOMPASSES` | `domain_encompasses` | Field covers application | Causal Inference → Policy Evaluation |
| `THEORY_APPLIED_BY` | `theory_applied_by` | Theory used by method | Judea Pearl → Difference-in-Differences |

#### OWL-Inspired Inferred Relations

| Relation | YAML Key | OWL Pattern | Description | Example |
|----------|----------|-------------|-------------|---------|
| `COAUTHOR_OF` | `coauthor_of` | owl:SymmetricProperty | Bidirectional collaboration | If A coauthor of B → B coauthor of A |
| `COLLABORATES_WITH` | `collaborates_with` | owl:SymmetricProperty | Bidirectional collaboration | If A collaborates with B → B collaborates with A |
| `CREATED_BY` | `created_by` | owl:inverseOf | Inverse of created | Theory → Creator |
| `USED_BY` | `used_by` | owl:inverseOf | Inverse of uses | Framework → Applications |
| `HAS_PART` | `has_part` | owl:inverseOf | Inverse of part_of | System → Components |
| `INHERITS_METHODOLOGY_FROM` | `inherits_methodology_from` | Property chain | Method inherits parent's technique | DiD inherits from Quasi-Experimental |
| `CONTRIBUTED_TO_FIELD` | `contributed_to_field` | Compositional | Field-level contribution | Pearl → Causal Inference |
| `BRIDGES_DOMAIN` | `bridges_domain` | Multi-field detection | Cross-disciplinary method | Econometrics bridges Economics & Statistics |
| `REQUIRES_UNDERSTANDING` | `requires_understanding` | Transitive dependency | Learning prerequisite chain | Advanced ML → Statistics → Probability |

**Note**: Inferred facts are added to the **subject** entity's file with `inferred_by: reasoner` metadata.

## 🧪 Testing

```bash
# Run the analyzer on the example knowledge base
python src/cli/analyze.py

# Test persistence (dry run recommended first)
python src/cli/persist.py
```

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── reasoning-workflow.yml    # GitHub Actions automation
├── src/
│   ├── obsidian_reasoner/            # Core modules
│   ├── cli/                          # CLI commands
│   └── importers/                    # Data importers
├── graph/                            # Your Obsidian vault
│   └── CausalInference/              # Example: Causal inference knowledge
├── requirements.txt                  # Python dependencies
├── setup.py                          # Package configuration
└── README.md                         # This file
```

## 🎯 Computational Ontology

This project follows a computational ontology design documented in Grafo:
- **Document**: `graphandmodel_computational_ontology`
- **IRI**: `http://www.graphandmodel.io/ontology`

Key architectural principles:
- No orphan entity nodes
- All relationships have attributes
- All entities have properties
- Modular separation: extraction → reasoning → persistence

## 🛠️ Development

### Adding New Inference Rules

Edit `src/obsidian_reasoner/reasoner.py` and add your rule method to the `GraphReasoner` class:

```python
def _rule_my_custom_rule(self, indexes: Dict) -> Set[tuple]:
    """Your custom reasoning rule."""
    inferred = set()
    # Your logic here
    return inferred
```

Then register it in `__init__`:

```python
self.rules = [
    # ... existing rules
    self._rule_my_custom_rule,
]
```

### Adding New Relationship Types

1. Update `RELATION_MAPPINGS` in `src/obsidian_reasoner/extractor.py`
2. Update `RELATION_TO_KEY` in `src/obsidian_reasoner/persister.py`

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🔗 Related Projects

- [Obsidian](https://obsidian.md/) - The knowledge base application
- [Grafo](https://gra.fo/) - Computational ontology platform
