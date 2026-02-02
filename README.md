# Reasoning Obsidian 

A reasoning engine applied to an Obsidian vault, automatically inferring new relationships and enriching the knowledge base.

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

**Automatic fact extraction**: Parses YAML frontmatter from Obsidian markdown files

**Logical reasoning**: Applies 12 inference rules (6 domain-specific + 6 OWL-inspired) to discover new relationships:

**Domain-specific rules:**
1. **Transitive parent** (ANCESTOR_OF): If A parent of B, and B parent of C → A ancestor of C
2. **Transitive part-of** (TRANSITIVELY_PART_OF): If A part of B, and B part of C → A transitively part of C
3. **Contribution** (CONTRIBUTED_TO): If Creator created X, and X part of Y → Creator contributed to Y
4. **Indirect usage** (INDIRECTLY_USES): If A uses X, and X uses Y → A indirectly uses Y
5. **Domain encompasses** (DOMAIN_ENCOMPASSES): If A parent of X, and X part of Y → A's domain encompasses Y
6. **Theory application** (THEORY_APPLIED_BY): If Creator created Theory, and Method uses Theory → Creator's theory applied by Method

**OWL-inspired rules:**
7. **Symmetric Collaboration** (COAUTHOR_OF, COLLABORATES_WITH): If A coauthor of B → B coauthor of A (symmetric property)
8. **Inverse Properties** (CREATED_BY, USED_BY, HAS_PART): Automatically generate inverse relationships (owl:inverseOf)
9. **Methodology Inheritance** (INHERITS_METHODOLOGY_FROM): If Method is_a ParentMethod, ParentMethod uses Technique → Method inherits from Technique
10. **Field Contribution** (CONTRIBUTED_TO_FIELD): If Person created Method, Method works_in Field → Person contributed to Field
11. **Cross-Domain Bridges** (BRIDGES_DOMAIN): Detects methods that integrate theories from multiple fields
12. **Prerequisite Chain** (REQUIRES_UNDERSTANDING): Creates transitive learning dependencies

**Automated discovery persistence**: writes inferred facts back to your Obsidian vault

**CI/CD Integration**: GitHub Actions automatically runs reasoning when you add new notes

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package (optional)
pip install -e .
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


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

